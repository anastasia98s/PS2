import torch.nn as nn
import torch
import sqlite3
from sklearn import preprocessing
import pandas as pd
import config

from torchmetrics import ConfusionMatrix
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
import torch

def show_conf_matrix(vorhersage_array, loesung_array, label, title, binary=False, plot=False):
    def calculate_accuracy(vorhersage_array, loesung_array):
        vorhersage_tensor = torch.tensor(vorhersage_array)
        loesung_tensor = torch.tensor(loesung_array)
        genauigkeit = (vorhersage_tensor == loesung_tensor).sum().item() / len(loesung_tensor)
        return round(genauigkeit * 100, 1)

    if len(label) > 1:
        title = title + "\nGenauigkeit: " + str(calculate_accuracy(vorhersage_array, loesung_array)) + "%"
        print("\nConfusion matrix " + title)
        if binary:
            confmat_metric = ConfusionMatrix(task='binary', num_classes=2)
        else:
            confmat_metric = ConfusionMatrix(task='multiclass', num_classes=len(label))
        conf_matrix = confmat_metric(torch.tensor(vorhersage_array), torch.tensor(loesung_array))
        print(conf_matrix)

        if plot:
            conf_matrix_np = conf_matrix.cpu().numpy()
            fig, ax = plot_confusion_matrix(conf_mat=conf_matrix_np, class_names=label, figsize=(8, 8), cmap="Blues")
            plt.tight_layout(pad=3.0)
            plt.title(title)
            plt.xlabel("Vorhersage")
            plt.ylabel("Lösung")
            plt.show()

        return conf_matrix
    else:
        return None

def to_yhat(logits):
    logits = logits.view(-1, logits.shape[-1]).cpu().detach()
    probs = torch.softmax(logits, dim=1)
    y_hat = torch.argmax(probs, dim=1)
    return probs.numpy(), y_hat.numpy()

class AbsichtSzenarioDataset:
    def __init__(self,text,absicht,szenario):
        self.texts = text 
        self.absicht = absicht
        self.szenario = szenario

        self.tokenizer = config.TEXTKLASSIFIZIERUNG_TOKENIZER
        self.max_len = config.TEXTKLASSIFIZIERUNG_MAX_LEN
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self,item):
        absicht = self.absicht[item]
        szenario = self.szenario[item]

        return {
            'target_absicht': torch.tensor(absicht, dtype=torch.long),
            'target_szenario': torch.tensor(szenario, dtype=torch.long)
        }
            
class AnmerkungDataset:
    def __init__(self, text, anmerkung):
        self.texts = text
        self.anmerkung = anmerkung
        #self.tokenizer = config.TEXTKLASSIFIZIERUNG_TOKENIZER
        self.max_len = config.TEXTKLASSIFIZIERUNG_MAX_LEN 
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self,index):
        ids = self.texts[index]
        target_anmerkung = self.anmerkung[index]

        ids = ids[:self.max_len-2]
        target_anmerkung = target_anmerkung[:self.max_len-2]

        ids = [101] + ids + [102]
        target_anmerkung = [0] + target_anmerkung + [0]
        
        mask, token_type_id = [1]*len(ids), [0]*len(ids)

        padding_len = self.max_len - len(ids)
        
        ids = ids + ([0] * padding_len)
        target_anmerkung = target_anmerkung + ([0] * padding_len)
        mask = mask + ([0] * padding_len)
        token_type_id = token_type_id + ([0] * padding_len)

        return {
            'ids': torch.tensor(ids, dtype=torch.long),
            'target_anmerkung': torch.tensor(target_anmerkung, dtype=torch.long),
            'mask': torch.tensor(mask, dtype=torch.long),
            'token_type_ids': torch.tensor(token_type_id, dtype=torch.long)
        }

class SatzDataset(torch.utils.data.Dataset):

    def __init__(self, text, anmerkung, absicht, szenario):
        self.texts = text
        self.anmerkung = anmerkung
        self.absicht = absicht
        self.szenario = szenario

        self.anmerkung_dataset = AnmerkungDataset(self.texts, self.anmerkung)
        
        self.absicht_szenario_dataset = AbsichtSzenarioDataset(self.texts, self.absicht, self.szenario)
    def __len__(self):
        return len(self.texts)

    def __getitem__(self,item):
        anmerkung_item = self.anmerkung_dataset[item] 
        absicht_szenario_item = self.absicht_szenario_dataset[item]
        
        return {
            'ids':anmerkung_item['ids'],
            'target_anmerkung': anmerkung_item['target_anmerkung'],
            'target_absicht': absicht_szenario_item['target_absicht'],
            'target_szenario':absicht_szenario_item['target_szenario'],
            'mask': anmerkung_item['mask'],
            'token_type_ids': anmerkung_item['token_type_ids'],
        }

def get_data(data_path):

    conn = sqlite3.connect(data_path)

    query = '''
        SELECT 
            sp_satz.satz_id AS satz_nr, 
            sp_wort.wort AS woerter, 
            sp_anmerkung.anmerkung_id AS anmerkungen,
            sp_anmerkung.is_bio_tag AS bio,
            sp_absicht.absicht_id AS absichten,
            sp_szenario.szenario_id AS szenarios
        FROM sp_satz
        JOIN sp_wort ON sp_satz.satz_id = sp_wort.satz_id
        JOIN sp_anmerkung ON sp_wort.anmerkung_id = sp_anmerkung.anmerkung_id
        JOIN sp_absicht ON sp_satz.absicht_id = sp_absicht.absicht_id
        JOIN sp_szenario ON sp_satz.szenario_id = sp_szenario.szenario_id
    '''
    
    df = pd.read_sql_query(query, conn)

    conn.close()

    tokenizer = config.TEXTKLASSIFIZIERUNG_TOKENIZER
    prev_satz_id = None
    prev_anmerkung_id = None
    rows_to_add = []

    for idx, row in df.iterrows():
        token_ids = tokenizer.encode(row['woerter'], add_special_tokens=False)
        for idx1, token_id in enumerate(token_ids):
            if idx1 == 0:
                df.at[idx, 'woerter'] = token_id
            else:
                new_row = {
                    'satz_nr': row['satz_nr'],
                    'woerter': token_id,
                    'anmerkungen': row['anmerkungen'],
                    'bio': row['bio'],
                    'absichten': row['absichten'],
                    'szenarios': row['szenarios']
                }
                rows_to_add.append((idx + 1, new_row))

    for index, new_row in reversed(rows_to_add):
        df = pd.concat([df.iloc[:index], pd.DataFrame([new_row]), df.iloc[index:]], ignore_index=True)


    for idx, row in df.iterrows():
        if row['satz_nr'] == prev_satz_id and prev_anmerkung_id == row['anmerkungen'] and row['bio'] == 1:
            df.at[idx, 'anmerkungen'] = -row['anmerkungen']

        prev_satz_id = row['satz_nr']
        prev_anmerkung_id = row['anmerkungen']

    encoder_anmerkung = preprocessing.LabelEncoder()
    df.loc[:, 'anmerkungen'] = encoder_anmerkung.fit_transform(df['anmerkungen'])

    encoder_absicht = preprocessing.LabelEncoder()
    df.loc[:,'absichten'] = encoder_absicht.fit_transform(df['absichten'])

    encoder_szenario = preprocessing.LabelEncoder()
    df.loc[:,'szenarios'] = encoder_szenario.fit_transform(df['szenarios'])

    satze = df.groupby('satz_nr')['woerter'].apply(list).values
    anmerkungen = df.groupby('satz_nr')['anmerkungen'].apply(list).values

    absicht = df.groupby('satz_nr')['absichten'].apply(lambda x: list(set(x))).values
    szenario = df.groupby('satz_nr')['szenarios'].apply(lambda x: list(set(x))).values

    return satze, anmerkungen, absicht, szenario, encoder_anmerkung, encoder_absicht, encoder_szenario

def loss_fn(logits, targets, mask, num_labels, anmerkung=False):
    criterion = nn.CrossEntropyLoss()
    
    if anmerkung:
        active_loss = mask.view(-1) == 1
        active_targets = torch.where(
            active_loss,
            targets.view(-1),
            torch.tensor(criterion.ignore_index).type_as(targets)
        )
        logits = logits.view(-1,num_labels)
        loss = criterion(logits, active_targets)
    else:
        loss = criterion(logits, targets.view(-1))

    return loss

def val_fn(data_loader, model,device, batch=None):
    model.eval()
    final_loss = 0
    preds_anmerkung_array = []
    loesung_anmerkung_array = []
    preds_absicht_array = []
    loesung_absicht_array = []
    preds_szenario_array = []
    loesung_szenario_array = []

    with torch.no_grad():
        for bi, batch in enumerate(data_loader):

            for k, v in batch.items():
                batch[k] = v.to(device)

            anmerkung_logits, absicht_logits, szenario_logits = model(batch['ids'], batch['mask'], batch['token_type_ids'])
            
            anmerkung_loss =  loss_fn(anmerkung_logits, batch['target_anmerkung'], batch['mask'],model.num_anmerkung, anmerkung=True)
            absicht_loss =  loss_fn(absicht_logits, batch['target_absicht'], batch['mask'],model.num_absicht)
            szenario_loss =  loss_fn(szenario_logits, batch['target_szenario'], batch['mask'],model.num_szenario)
            
            loss = (anmerkung_loss + absicht_loss + szenario_loss)/3
            final_loss += loss

            #preds_anmerkung_array = []
            #loesung_anmerkung_array = []
            for index in range(len(anmerkung_logits)):
                active_mask = batch['mask'][index] == 1
                _, preds_anmerkung = torch.max(anmerkung_logits[index], dim=-1)
                active_preds_anmerkung = preds_anmerkung[active_mask]
                active_target_anmerkung = batch['target_anmerkung'][index][active_mask]

                active_ids = batch['ids'][index][active_mask]
                filter_ids = (active_ids != 101) & (active_ids != 102)
                preds_anmerkung_array.append(active_preds_anmerkung[filter_ids])
                loesung_anmerkung_array.append(active_target_anmerkung[filter_ids])

            _, preds_absicht = to_yhat(absicht_logits)
            _, preds_szenario = to_yhat(szenario_logits)

            preds_absicht_array.extend(preds_absicht)
            loesung_absicht_array.extend(batch['target_absicht'].view(-1))

            preds_szenario_array.extend(preds_szenario)
            loesung_szenario_array.extend(batch['target_szenario'].view(-1))

    return final_loss/len(data_loader), preds_anmerkung_array, loesung_anmerkung_array, preds_absicht_array, loesung_absicht_array, preds_szenario_array, loesung_szenario_array

def train_fn(data_loader,
             model,
             optimizer,
             scheduler,
             device,
             batch = None
            ):

    model.train()
    final_loss = 0

    for bi, batch in enumerate(data_loader):
        for k,v in batch.items():
            batch[k] = v.to(device)

        optimizer.zero_grad()

        anmerkung_logits, absicht_logits, szenario_logits =  model(batch['ids'], batch['mask'], batch['token_type_ids'])
        
        anmerkung_loss =  loss_fn(anmerkung_logits, batch['target_anmerkung'], batch['mask'], model.num_anmerkung, anmerkung=True)
        absicht_loss =  loss_fn(absicht_logits, batch['target_absicht'], batch['mask'], model.num_absicht)
        szenario_loss =  loss_fn(szenario_logits, batch['target_szenario'], batch['mask'], model.num_szenario)

        loss = (anmerkung_loss + absicht_loss + szenario_loss)/3

        loss.backward()
        
        nn.utils.clip_grad_norm_(model.parameters(), max_norm = 1.0)
        
        optimizer.step()
        
        scheduler.step()

        final_loss += loss.item()

    return final_loss/len(data_loader)
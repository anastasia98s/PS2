import torch.nn as nn
import torch
import sqlite3
from sklearn import preprocessing
import pandas as pd
import config

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
        self.tokenizer = config.TEXTKLASSIFIZIERUNG_TOKENIZER
        self.max_len = config.TEXTKLASSIFIZIERUNG_MAX_LEN 
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self,item):
        text = self.texts[item]
        anmerkung = self.anmerkung[item]
        
        ids = []
        target_anmerkung = []
        for i,wort in enumerate(text):
            token_ids = self.tokenizer.encode(wort, add_special_tokens=False)
            wort_piece_anmerkung = [anmerkung[i]] * len(token_ids)

            ids.extend(token_ids)
            target_anmerkung.extend(wort_piece_anmerkung)

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

        self.anmerkung_dataset = AnmerkungDataset(self.texts,
                                            self.anmerkung)
        
        self.absicht_szenario_dataset = AbsichtSzenarioDataset(
                                                                self.texts,
                                                                self.absicht,
                                                                self.szenario
                                                            )
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
            sp_anmerkung.anmerkung AS anmerkungen,
            sp_absicht.absicht AS absichten,
            sp_szenario.szenario AS szenarios
        FROM sp_satz
        JOIN sp_wort ON sp_satz.satz_id = sp_wort.satz_id
        JOIN sp_anmerkung ON sp_wort.anmerkung_id = sp_anmerkung.anmerkung_id
        JOIN sp_absicht ON sp_satz.absicht_id = sp_absicht.absicht_id
        JOIN sp_szenario ON sp_satz.szenario_id = sp_szenario.szenario_id
    '''
    
    df = pd.read_sql_query(query, conn)

    conn.close()

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

    with torch.no_grad():
        for bi, batch in enumerate(data_loader):

            for k, v in batch.items():
                batch[k] = v.to(device)

            (
                anmerkung_logits,
                absicht_logits,
                szenario_logits) = model(
                                            batch['ids'], 
                                            batch['mask'],
                                            batch['token_type_ids'])
            
            anmerkung_loss =  loss_fn(anmerkung_logits,batch['target_anmerkung'],batch['mask'],model.num_anmerkung, anmerkung=True)
            absicht_loss =  loss_fn(absicht_logits,batch['target_absicht'],batch['mask'],model.num_absicht)
            szenario_loss =  loss_fn(szenario_logits,batch['target_szenario'],batch['mask'],model.num_szenario)
            
            loss = (anmerkung_loss + absicht_loss + szenario_loss)/3
            final_loss += loss

    return final_loss/len(data_loader)

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

        # zero
        optimizer.zero_grad()

        # Forward
        (
            anmerkung_logits,
            absicht_logits,
            szenario_logits) =  model(
                                        batch['ids'], 
                                        batch['mask'],
                                        batch['token_type_ids']
                                    )
        # loss
        anmerkung_loss =  loss_fn(anmerkung_logits, batch['target_anmerkung'], batch['mask'], model.num_anmerkung, anmerkung=True)
        absicht_loss =  loss_fn(absicht_logits, batch['target_absicht'], batch['mask'], model.num_absicht)
        szenario_loss =  loss_fn(szenario_logits, batch['target_szenario'], batch['mask'], model.num_szenario)

        loss = (anmerkung_loss + absicht_loss + szenario_loss)/3

        # Backward
        loss.backward()
        
        nn.utils.clip_grad_norm_(model.parameters(), max_norm = 1.0)
        
        optimizer.step()
        
        scheduler.step()

        final_loss += loss.item()

    return final_loss/len(data_loader)
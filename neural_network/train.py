import torch
from torch.utils.data import DataLoader
from torch import optim
from transformers import get_linear_schedule_with_warmup
import joblib

import pandas as pd 
import numpy as np
from sklearn import preprocessing
from sklearn import model_selection
import sqlite3

import config
import neural_network.utils
from neural_network.dataset import NLUDataset 
from neural_network.model import Model

def process_data(data_path):

    conn = sqlite3.connect(data_path)

    query = '''
        SELECT 
            sp_satz.satz_id AS "satz_nr", 
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

    enc_anmerkung = preprocessing.LabelEncoder()
    df.loc[:, 'anmerkungen'] = enc_anmerkung.fit_transform(df['anmerkungen'])

    enc_absicht = preprocessing.LabelEncoder()
    df.loc[:,'absichten'] = enc_absicht.fit_transform(df['absichten'])

    enc_szenario = preprocessing.LabelEncoder()
    df.loc[:,'szenarios'] = enc_szenario.fit_transform(df['szenarios'])

    satze = df.groupby('satz_nr')['woerter'].apply(list).values
    entities = df.groupby('satz_nr')['anmerkungen'].apply(list).values
    # len_upper = len(max(satze, key=len))

    absicht = df.groupby('satz_nr')['absichten'].apply(lambda x: list(set(x))).values
    szenario = df.groupby('satz_nr')['szenarios'].apply(lambda x: list(set(x))).values

    # len_absicht = df['absichten'].nunique()
    # len_szenario = df['szenarios'].nunique()
    # len_entities = df['anmerkungen'].nunique()
    
    return satze, entities, absicht, szenario, enc_anmerkung, enc_absicht, enc_szenario

def run():
    
    satze, target_anmerkung , target_absicht, target_szenario, enc_anmerkung, enc_absicht, enc_szenario = process_data(config.DATASET_PATH) #er_data
    
    num_anmerkung, num_absicht, num_szenario = len(enc_anmerkung.classes_),len(enc_absicht.classes_),len(enc_szenario.classes_)
    
    meta_data = {
        'enc_anmerkung': enc_anmerkung,
        'enc_absicht': enc_absicht,
        'enc_szenario': enc_szenario
    }
    joblib.dump(meta_data, config.META_PATH)

    # print(len(satze), len(target_anmerkung), len(target_absicht), len(target_szenario))
 
    (
        train_satze,
        val_satze,
        train_anmerkung,
        val_anmerkung,
        train_absicht,
        val_absicht,
        train_szenario,
        val_szenario) = model_selection.train_test_split( # train validation 
                                                        satze,
                                                        target_anmerkung,
                                                        target_absicht,
                                                        target_szenario,
                                                        random_state=50,
                                                        test_size=0.1,
                                                        #stratify=train_absicht
                                                    )
    # train
    train_dataset = NLUDataset(train_satze,
                               train_anmerkung,
                               train_absicht,
                               train_szenario)
    
    train_data_loader = DataLoader(train_dataset,
                                   batch_size = config.TRAIN_BATCH_SIZE,
                                   num_workers= 4)
    
    # validation
    val_dataset = NLUDataset(val_satze,
                               val_anmerkung,
                               val_absicht,
                               val_szenario)
    
    val_data_loader = DataLoader(val_dataset,
                                 batch_size = config.TRAIN_BATCH_SIZE,
                                 num_workers= 4)
        
    device = config.DEVICE 
    net = Model(num_anmerkung, num_absicht, num_szenario)
    net.to(device)

    if config.RETRAIN_MODEL:
        net.load_state_dict(torch.load(config.TRAINED_PATH))

    num_train_steps = config.TRAIN_BATCH_SIZE * config.EPOCHS
    optimizer = optim.AdamW(net.parameters(), lr=2e-5, weight_decay=0.01)
    scheduler =  get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps = 0,
        num_training_steps = num_train_steps
    )
    
    best_loss = np.inf
    
    print("=" * 10)
    print(f'Training Data: {len(train_satze)}')
    print(f'Validation Data: {len(val_satze)}')
    print(f'Total Data: {len(val_satze)}')
    
    for epoch in range(config.EPOCHS):
        print(f'\n== Epoch {epoch + 1}/{config.EPOCHS}')
  
        train_loss = neural_network.utils.train_fn(
                                                train_data_loader,
                                                net,
                                                optimizer,
                                                scheduler,
                                                device
                                            )
        
        print(f'Train Loss:{train_loss}')
        
        val_loss = neural_network.utils.eval_fn(
                                            val_data_loader,
                                            net,
                                            device
                                        )

        print(f'Valid Loss:{val_loss}')

        if val_loss < best_loss and config.SAVE_MODEL:
            torch.save(net.state_dict(), config.TRAINED_PATH)
            best_loss = val_loss
            print(f'neues Model: Epoch {epoch}, Loss: {best_loss}')
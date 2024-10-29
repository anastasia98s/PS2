import json
import torch
import sqlite3
import librosa
import numpy as np
import pandas as pd
import torch.nn as nn
from sklearn import preprocessing

class merkmaleDataset(torch.utils.data.Dataset):
    def __init__(self, merkmale, namen):
        self.merkmale = merkmale
        self.namen = namen

    def __len__(self):
        return len(self.merkmale)

    def __getitem__(self, idx):
        merkmale = torch.tensor(self.merkmale[idx], dtype=torch.float32)
        namen = torch.tensor(self.namen[idx], dtype=torch.int64)
        return merkmale, namen

def extract_features(signal, sample_rate):
    mfccs = np.mean(librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=40).T, axis=0)
    stft = np.abs(librosa.stft(signal))
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(y=signal, sr=sample_rate).T, axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(signal), sr=sample_rate).T, axis=0)
    return np.hstack([mfccs, chroma, mel, contrast, tonnetz])

def get_data(data_path):
    with sqlite3.connect(data_path) as conn:
        query = '''
            SELECT 
                sp_benutzer.benutzer_id AS benutzer, 
                sp_merkmale.merkmale AS merkmale
            FROM sp_benutzer
            JOIN sp_merkmale ON sp_benutzer.benutzer_id = sp_merkmale.benutzer_id
        '''
        df = pd.read_sql_query(query, conn)
        
    encoder_name = preprocessing.LabelEncoder()
    df['benutzer'] = encoder_name.fit_transform(df['benutzer'])
    namen = df['benutzer'].values
    df['merkmale'] = df['merkmale'].apply(json.loads)
    merkmale = np.array(df['merkmale'].tolist())
    return merkmale, namen, encoder_name

loss_fn = nn.CrossEntropyLoss()

def train_fn(data_loader,
             model,
             optimizer,
             device):
    
    model.train()
    final_loss = 0

    for batch in data_loader:
        merkmale, namen = batch
        merkmale = merkmale.to(device)
        namen = namen.to(device)

        # zero
        optimizer.zero_grad()

        # Forward
        output = model(merkmale)
        
        # loss
        loss = loss_fn(output, namen)

        # Backward
        loss.backward()
        
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        
        final_loss += loss.item()

    return final_loss/len(data_loader)

def val_fn( data_loader,
            model,
            device):
    
    model.eval()
    final_loss = 0

    with torch.no_grad():
        for batch in data_loader:
            merkmale, namen = batch
            merkmale = merkmale.to(device)
            namen = namen.to(device)

            # Forward
            output =  model(merkmale)
            
            # loss
            loss =  loss_fn(output, namen)
 
            final_loss += loss.item()

    return final_loss/len(data_loader)

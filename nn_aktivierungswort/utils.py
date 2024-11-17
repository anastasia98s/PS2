import json
import torch
import sqlite3
import librosa
import numpy as np
import pandas as pd
import torch.nn as nn

class merkmaleDataset(torch.utils.data.Dataset):
    def __init__(self, merkmale, labels):
        self.merkmale = merkmale
        self.labels = labels

    def __len__(self):
        return len(self.merkmale)

    def __getitem__(self, idx):
        merkmale = torch.tensor(self.merkmale[idx], dtype=torch.float32)
        labels = torch.tensor(self.labels[idx], dtype=torch.float32)
        return merkmale, labels

def extract_features(signal, sample_rate):
    signal = (signal - np.mean(signal)) / np.std(signal)
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
                sp_aktivierungswort_merkmale.typ AS typ, 
                sp_aktivierungswort_merkmale.aktivierungswort_merkmale AS merkmale
            FROM sp_aktivierungswort_merkmale
        '''
        df = pd.read_sql_query(query, conn)
        
    labels = df['typ'].values
    df['merkmale'] = df['merkmale'].apply(json.loads)
    merkmale = np.array(df['merkmale'].tolist())
    return merkmale, labels

loss_fn = nn.BCEWithLogitsLoss()

def train_fn(data_loader,
             model,
             optimizer,
             device):
    
    model.train()
    final_loss = 0

    for batch in data_loader:
        merkmale, labels = batch
        merkmale = merkmale.to(device)
        labels = labels.to(device)

        # zero
        optimizer.zero_grad()

        # Forward
        output = model(merkmale)

        # loss
        loss = loss_fn(output, labels)

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
            merkmale, labels = batch
            merkmale = merkmale.to(device)
            labels = labels.to(device)

            # Forward
            output =  model(merkmale)
            
            # loss
            loss =  loss_fn(output, labels)
 
            final_loss += loss.item()

    return final_loss/len(data_loader)

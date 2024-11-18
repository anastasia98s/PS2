import json
import torch
import sqlite3
import librosa
import numpy as np
import pandas as pd
import torch.nn as nn

class MerkmaleDataset(torch.utils.data.Dataset):
    def __init__(self, merkmale, labels):
        self.merkmale = merkmale
        self.labels = labels

    def __len__(self):
        return len(self.merkmale)

    def __getitem__(self, idx):
        merkmale = torch.tensor(self.merkmale[idx], dtype=torch.float32)
        labels = torch.tensor(self.labels[idx], dtype=torch.float32)
        return merkmale, labels

def extract_features(signal, sample_rate, n_mels=128, hop_length=512, n_fft=2048, duration=2):
    target_length = int(duration * sample_rate)
    if len(signal) < target_length:
        signal = np.pad(signal, (0, target_length - len(signal)), mode='constant')
    else:
        signal = signal[:target_length]
    
    mel_spectrogram = librosa.feature.melspectrogram(
        y=signal,
        sr=sample_rate,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels
    )

    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    return mel_spectrogram_db

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

loss_fn = nn.BCELoss() #BCEWithLogitsLoss

def train_fn(data_loader,
             model,
             optimizer,
             device):
    
    model.train()
    final_loss = 0

    for batch in data_loader:
        merkmale, labels = batch
        merkmale = merkmale.to(device).unsqueeze(1)
        labels = labels.to(device).unsqueeze(1)

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
    preds_aktivierung_array = []
    loesung_aktivierung_array = []

    with torch.no_grad():
        for batch in data_loader:
            merkmale, labels = batch
            merkmale = merkmale.to(device).unsqueeze(1)
            labels = labels.to(device).unsqueeze(1)
            # Forward
            output =  model(merkmale)
            
            # loss
            loss =  loss_fn(output, labels)
 
            final_loss += loss.item()

            preds_aktivierung_array.extend(torch.round(output))
            loesung_aktivierung_array.extend(labels)

    return final_loss/len(data_loader), preds_aktivierung_array, loesung_aktivierung_array

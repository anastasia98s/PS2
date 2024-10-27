import torch
import librosa
import numpy as np
import pandas as pd
import torch.nn as nn
from sklearn import preprocessing

class AudioDataset(torch.utils.data.Dataset):
    def __init__(self, audio, namen):
        self.audio = audio
        self.namen = namen

    def __len__(self):
        return len(self.audio)

    def __getitem__(self, idx):
        audio = torch.tensor(self.audio[idx], dtype=torch.float32)
        namen = torch.tensor(self.namen[idx], dtype=torch.int64)
        return audio, namen

def extract_features(signal, sample_rate):
    mfccs = np.mean(librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=40).T, axis=0)
    stft = np.abs(librosa.stft(signal))
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(y=signal, sr=sample_rate).T, axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(signal), sr=sample_rate).T, axis=0)
    return np.hstack([mfccs, chroma, mel, contrast, tonnetz])

def save_features_to_csv(filename, features, name):
    feature_columns = ['f' + str(i) for i in range(1, len(features) + 1)]
    df = pd.DataFrame([[name] + features.tolist()], columns=['name'] + feature_columns)
    df.to_csv(filename, mode='a', index=False, header=not pd.io.common.file_exists(filename))
    print("gespeichert!")

def get_data(data_path):
    df = pd.read_csv(data_path)
    audios = df.drop(columns=['name']).values
    encoder_name = preprocessing.LabelEncoder()
    df.loc[:, 'name'] = encoder_name.fit_transform(df['name'])
    namen = df['name'].values

    return audios, namen, encoder_name

loss_fn = nn.CrossEntropyLoss()

def train_fn(data_loader,
             model,
             optimizer,
             device):
    
    model.train()
    final_loss = 0

    for batch in data_loader:
        audios, namen = batch
        audios = audios.to(device)
        namen = namen.to(device)

        # zero
        optimizer.zero_grad()

        # Forward
        output = model(audios)
        
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
            audios, namen = batch
            audios = audios.to(device)
            namen = namen.to(device)

            # Forward
            output =  model(audios)
            
            # loss
            loss =  loss_fn(output, namen)
 
            final_loss += loss.item()

    return final_loss/len(data_loader)

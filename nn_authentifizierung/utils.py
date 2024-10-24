import torch
import sounddevice as sd
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

def record_voice(duration=5):
    print("Rec...")
    recording = sd.rec(int(duration * 44100), samplerate=44100, channels=1, dtype='float64')
    sd.wait()
    print("End")
    return recording.flatten()

def extract_features(signal):
    top_db = 5
    sr = 44100
    non_silent = librosa.effects.split(signal, top_db=top_db)
    if len(non_silent) == 0:
        return np.zeros((13,))
    non_silent_signal = np.concatenate([signal[start:end] for start, end in non_silent])
    return librosa.feature.mfcc(y=non_silent_signal, sr=sr, n_mfcc=13)

""" def mean_extract_features(signal):
    return np.mean(extract_features(signal).T, axis=0) """

def get_data(data_path):
    df = pd.read_csv(data_path)
    audios = df.drop(columns=['Name']).values
    encoder_name = preprocessing.LabelEncoder()
    df.loc[:, 'Name'] = encoder_name.fit_transform(df['Name'])
    namen = df['Name'].values

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

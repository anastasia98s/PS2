import json
import torch
import sqlite3
import librosa
import numpy as np
import pandas as pd
import torch.nn as nn
from sklearn import preprocessing
import nn_authentifizierung.utils

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

class MerkmaleDataset(torch.utils.data.Dataset):
    def __init__(self, merkmale, benutzerids):
        self.merkmale = merkmale
        self.benutzerids = benutzerids

    def __len__(self):
        return len(self.merkmale)

    def __getitem__(self, idx):
        merkmale = torch.tensor(self.merkmale[idx], dtype=torch.float32)
        benutzerids = torch.tensor(self.benutzerids[idx], dtype=torch.int64)
        return merkmale, benutzerids

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
    benutzerids = df['benutzer'].values
    df['merkmale'] = df['merkmale'].apply(json.loads)
    merkmale = np.array(df['merkmale'].tolist())
    return merkmale, benutzerids, encoder_name

loss_fn = nn.CrossEntropyLoss()

def train_fn(data_loader,
             model,
             optimizer,
             device):
    
    model.train()
    final_loss = 0

    for batch in data_loader:
        merkmale, benutzerids = batch
        merkmale = merkmale.to(device)
        benutzerids = benutzerids.to(device)

        # zero
        optimizer.zero_grad()

        # Forward
        output = model(merkmale)
        
        # loss
        loss = loss_fn(output, benutzerids)

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
    preds_authentifizierung_array = []
    loesung_authentifizierung_array = []

    with torch.no_grad():
        for batch in data_loader:
            merkmale, benutzerids = batch
            merkmale = merkmale.to(device)
            benutzerids = benutzerids.to(device)

            # Forward
            output =  model(merkmale)
            
            # loss
            loss =  loss_fn(output, benutzerids)
 
            final_loss += loss.item()

            _, preds_benutzerids = nn_authentifizierung.utils.to_yhat(output)

            preds_authentifizierung_array.extend(preds_benutzerids)
            loesung_authentifizierung_array.extend(benutzerids)

    return final_loss/len(data_loader), preds_authentifizierung_array, loesung_authentifizierung_array

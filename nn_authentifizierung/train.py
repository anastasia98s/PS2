import os
import time
import joblib
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split

import config
import nn_authentifizierung.utils
from nn_authentifizierung.model import Model

def train():
    audios, namen, encoder_namen = nn_authentifizierung.utils.get_data(config.AUTHENTIFIZIERUNG_DATASET_PATH)
    meta_data = {
        'encoder_namen': encoder_namen
    }
    joblib.dump(meta_data, config.AUTHENTIFIZIERUNG_META_PATH)
    
    train_audios, val_audios, train_namen, val_namen = train_test_split(audios, namen, test_size=0.2, random_state=42, stratify=namen)

    train_dataset = nn_authentifizierung.utils.AudioDataset(train_audios, train_namen)
    train_data_loader = DataLoader( train_dataset,
                                    batch_size=config.AUTHENTIFIZIERUNG_TRAIN_BATCH_SIZE,
                                    shuffle=True,
                                    pin_memory=True,
                                    num_workers=4)
    
    val_dataset = nn_authentifizierung.utils.AudioDataset(val_audios, val_namen)
    val_data_loader = DataLoader(   val_dataset,
                                    batch_size=config.AUTHENTIFIZIERUNG_VALIDATION_BATCH_SIZE,
                                    shuffle=False,
                                    pin_memory=True,
                                    num_workers=4)
    
    num_namen = len(encoder_namen.classes_)

    device = config.DEVICE 
    model = Model(num_namen, config.AUTHENTIFIZIERUNG_HIDDEN_UNITS_1, config.AUTHENTIFIZIERUNG_HIDDEN_UNITS_2)
    model.to(device)

    if config.AUTHENTIFIZIERUNG_RETRAIN_MODEL:
        try:
            model.load_state_dict(torch.load(config.AUTHENTIFIZIERUNG_TRAINED_PATH))
            print("\n!!!Retraining!!!")
        except Exception as e:
            print(f"\nFehler beim Laden des Modells für das Retraining: {e}")

    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=0.01)

    start_zeit = time.time()

    best_loss = float('inf')

    print("=" * 10)
    print("Device: " + str(device))
    print(f'Training Data: {len(train_audios)}')
    print(f'Validation Data: {len(val_audios)}')
    print(f'Total Data: {len(audios)}')

    for epoch in range(config.AUTHENTIFIZIERUNG_EPOCHS):
        print(f'\n== Epoch {epoch + 1}/{config.AUTHENTIFIZIERUNG_EPOCHS}')
  
        train_loss = nn_authentifizierung.utils.train_fn(
                                                train_data_loader,
                                                model,
                                                optimizer,
                                                device)
        
        print(f'Train Loss: {train_loss}')

        val_loss = nn_authentifizierung.utils.val_fn(
                                            val_data_loader,
                                            model,
                                            device
                                        )

        if val_loss < best_loss and config.AUTHENTIFIZIERUNG_SAVE_MODEL:
            os.makedirs(os.path.dirname(config.AUTHENTIFIZIERUNG_TRAINED_PATH), exist_ok=True)
            torch.save(model.state_dict(), config.AUTHENTIFIZIERUNG_TRAINED_PATH)
            best_loss = val_loss
            print(f'Validation Loss: {best_loss}, neues Model: Epoch {epoch + 1}')
        else:
            print(f'Validation Loss: {val_loss}')

    end_zeit = time.time()

    trainingsdauer = (end_zeit - start_zeit) / 60

    print(f"\nTrainingsdauer: {trainingsdauer:.2f} Minuten")
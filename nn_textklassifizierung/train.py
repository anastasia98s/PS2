import torch
from torch.utils.data import DataLoader
from torch import optim
from transformers import get_linear_schedule_with_warmup
import joblib
import os
import time

import numpy as np
from sklearn import model_selection

import config
import nn_textklassifizierung.utils
from nn_textklassifizierung.model import Model

def train():
    
    satze, target_anmerkung , target_absicht, target_szenario, encoder_anmerkung, encoder_absicht, encoder_szenario = nn_textklassifizierung.utils.get_data(config.TEXTKLASSIFIZIERUNG_DATASET_PATH) #er_data
    
    num_anmerkung, num_absicht, num_szenario = len(encoder_anmerkung.classes_),len(encoder_absicht.classes_),len(encoder_szenario.classes_)
    
    meta_data = {
        'encoder_anmerkung': encoder_anmerkung,
        'encoder_absicht': encoder_absicht,
        'encoder_szenario': encoder_szenario
    }
    
    joblib.dump(meta_data, config.TEXTKLASSIFIZIERUNG_META_PATH)
 
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
                                                        random_state=42,
                                                        test_size=0.1,
                                                        # stratify=target_absicht
                                                    )
    # train
    train_dataset = nn_textklassifizierung.utils.SatzDataset(train_satze,
                               train_anmerkung,
                               train_absicht,
                               train_szenario)
    
    train_data_loader = DataLoader(train_dataset,
                                   batch_size=config.TEXTKLASSIFIZIERUNG_TRAIN_BATCH_SIZE,
                                   shuffle=True,
                                   num_workers=4)
    
    # validation
    val_dataset = nn_textklassifizierung.utils.SatzDataset(val_satze,
                               val_anmerkung,
                               val_absicht,
                               val_szenario)
    
    val_data_loader = DataLoader(val_dataset,
                                 batch_size = config.TEXTKLASSIFIZIERUNG_VALIDATION_BATCH_SIZE,
                                 shuffle=False,
                                 num_workers=4)
        
    device = config.DEVICE
    model = Model(num_anmerkung, num_absicht, num_szenario)
    model.to(device)

    if config.TEXTKLASSIFIZIERUNG_RETRAIN_MODEL:
        try:
            model.load_state_dict(torch.load(config.TEXTKLASSIFIZIERUNG_TRAINED_PATH))
            print("\n!!!Retraining!!!")
        except Exception as e:
            print(f"\nFehler beim Laden des Modells für das Retraining: {e}")

    num_train_steps = config.TEXTKLASSIFIZIERUNG_TRAIN_BATCH_SIZE * config.TEXTKLASSIFIZIERUNG_EPOCHS
    optimizer = optim.AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)
    scheduler =  get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps = 0,
        num_training_steps = num_train_steps
    )
    
    best_loss = np.inf
    
    print("=" * 10)
    print("Device: " + str(device))
    print(f'Training Data: {len(train_satze)}')
    print(f'Validation Data: {len(val_satze)}')
    print(f'Total Data: {len(satze)}')

    start_zeit = time.time()
    
    for epoch in range(config.TEXTKLASSIFIZIERUNG_EPOCHS):
        print(f'\n== Epoch {epoch + 1}/{config.TEXTKLASSIFIZIERUNG_EPOCHS}')
  
        train_loss = nn_textklassifizierung.utils.train_fn(
                                                train_data_loader,
                                                model,
                                                optimizer,
                                                scheduler,
                                                device
                                            )
        
        print(f'Train Loss: {train_loss}')
        
        val_loss = nn_textklassifizierung.utils.val_fn(
                                            val_data_loader,
                                            model,
                                            device
                                        )

        if val_loss < best_loss and config.TEXTKLASSIFIZIERUNG_SAVE_MODEL:
            os.makedirs(os.path.dirname(config.TEXTKLASSIFIZIERUNG_TRAINED_PATH), exist_ok=True)
            torch.save(model.state_dict(), config.TEXTKLASSIFIZIERUNG_TRAINED_PATH)
            best_loss = val_loss
            print(f'Validation Loss: {best_loss}, neues Model: Epoch {epoch}')
        else:
            print(f'Validation Loss: {val_loss}')
    
    end_zeit = time.time()

    trainingsdauer = (end_zeit - start_zeit) / 60

    print(f"\nTrainingsdauer: {trainingsdauer:.2f} Minuten")
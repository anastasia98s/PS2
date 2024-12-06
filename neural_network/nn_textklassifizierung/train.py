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
import neural_network.nn_textklassifizierung.utils
from neural_network.nn_textklassifizierung.model import Model
import neural_network.utils

def train():
    if not os.path.isfile(config.TEXTKLASSIFIZIERUNG_DATASET_PATH):
        raise FileNotFoundError(f"\ndie Datenbank ist leer")
    
    from utils.data_controller.textklassifizierung_controller.presenter import PresenterTextklassifizierung
    presenter_textklassifizierung = PresenterTextklassifizierung()
    
    satze, target_anmerkung , target_absicht, target_szenario, encoder_anmerkung, encoder_absicht, encoder_szenario = neural_network.nn_textklassifizierung.utils.get_data(config.TEXTKLASSIFIZIERUNG_DATASET_PATH) #er_data
    
    num_anmerkung, num_absicht, num_szenario = len(encoder_anmerkung.classes_),len(encoder_absicht.classes_),len(encoder_szenario.classes_)
    
    meta_data = {
        'encoder_anmerkung': encoder_anmerkung,
        'encoder_absicht': encoder_absicht,
        'encoder_szenario': encoder_szenario
    }
    
    joblib.dump(meta_data, config.TEXTKLASSIFIZIERUNG_META_PATH)
 
    train_satze, val_satze, train_anmerkung, val_anmerkung, train_absicht, val_absicht, train_szenario, val_szenario = model_selection.train_test_split(satze, target_anmerkung, target_absicht, target_szenario, random_state=42, test_size=0.1, stratify=target_szenario) # stratify=target_absicht
    
    # train
    train_dataset = neural_network.nn_textklassifizierung.utils.SatzDataset(train_satze, train_anmerkung, train_absicht, train_szenario)
    
    train_data_loader = DataLoader(train_dataset, batch_size=config.TEXTKLASSIFIZIERUNG_TRAIN_BATCH_SIZE, shuffle=True)
    
    # validation
    val_dataset = neural_network.nn_textklassifizierung.utils.SatzDataset(val_satze, val_anmerkung, val_absicht, val_szenario)
    
    val_data_loader = DataLoader(val_dataset, batch_size = config.TEXTKLASSIFIZIERUNG_VALIDATION_BATCH_SIZE, shuffle=False)
        
    device = config.DEVICE
    model = Model(num_anmerkung, num_absicht, num_szenario)
    model.to(device)

    if config.TEXTKLASSIFIZIERUNG_RETRAIN_MODEL:
        try:
            model.load_state_dict(torch.load(config.TEXTKLASSIFIZIERUNG_TRAINED_PATH, map_location=torch.device(config.DEVICE)))
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
    best_epochs = 1
    best_preds_anmerkung_array = []
    best_loesung_anmerkung_array = []
    best_preds_absicht_array = []
    best_loesung_absicht_array = []
    best_preds_szenario_array = []
    best_loesung_szenario_array = []
    zwillinge_anmerkung_len = (len(encoder_anmerkung.classes_) - 1)/2
    positive_anmerkung_class = [num for num in encoder_anmerkung.classes_ if num >= 0]
    confusion_matrix_anmerkung_class = [presenter_textklassifizierung.such_anmerkung(num) for num in positive_anmerkung_class]
    confusion_matrix_absicht_class = [presenter_textklassifizierung.such_absicht(num) for num in encoder_absicht.classes_]
    confusion_matrix_szenario_class = [presenter_textklassifizierung.such_szenario(num) for num in encoder_szenario.classes_]
    
    print("=" * 10)
    print("Device: " + str(device))
    print(f'Training Data: {len(train_satze)}')
    print(f'Validation Data: {len(val_satze)}')
    print(f'Total Data: {len(satze)}')

    start_zeit = time.time()
    
    for epoch in range(config.TEXTKLASSIFIZIERUNG_EPOCHS):
        print(f'\n== Epoch {epoch + 1}/{config.TEXTKLASSIFIZIERUNG_EPOCHS}')
  
        train_loss = neural_network.nn_textklassifizierung.utils.train_fn(train_data_loader, model, optimizer, scheduler, device)
        
        print(f'Train Loss: {train_loss}')
        
        val_loss, raw_preds_anmerkung_array, raw_loesung_anmerkung_array, preds_absicht_array, loesung_absicht_array, preds_szenario_array, loesung_szenario_array = neural_network.nn_textklassifizierung.utils.val_fn(val_data_loader, model, device)

        if val_loss < best_loss and config.TEXTKLASSIFIZIERUNG_SAVE_MODEL:
            
            preds_anmerkung_array = []
            loesung_anmerkung_array = []
            for index in range(len(raw_preds_anmerkung_array)):
                preds_anmerkung_array_tmp = [num + (zwillinge_anmerkung_len - num) * 2 if num < zwillinge_anmerkung_len else num for num in raw_preds_anmerkung_array[index]]
                loesung_anmerkung_array_tmp = [num + (zwillinge_anmerkung_len - num) * 2 if num < zwillinge_anmerkung_len else num for num in raw_loesung_anmerkung_array[index]]

                #print([num - zwillinge_anmerkung_len for num in preds_anmerkung_array])
                preds_anmerkung_array.append([num - zwillinge_anmerkung_len for num in preds_anmerkung_array_tmp])
                loesung_anmerkung_array.append([num - zwillinge_anmerkung_len for num in loesung_anmerkung_array_tmp])

            best_preds_anmerkung_array = preds_anmerkung_array
            best_loesung_anmerkung_array = loesung_anmerkung_array
            best_preds_absicht_array = preds_absicht_array
            best_loesung_absicht_array = loesung_absicht_array
            best_preds_szenario_array = preds_szenario_array
            best_loesung_szenario_array = loesung_szenario_array

            preds_anmerkung_array = [item for sublist in preds_anmerkung_array for item in sublist] #torch.cat(preds_anmerkung_array)
            loesung_anmerkung_array = [item for sublist in loesung_anmerkung_array for item in sublist] # torch.cat(loesung_anmerkung_array)

            neural_network.utils.show_conf_matrix(preds_anmerkung_array, loesung_anmerkung_array, confusion_matrix_anmerkung_class, "Textklassifizierung-KI (Anmerkung)")
            neural_network.utils.show_conf_matrix(preds_absicht_array, loesung_absicht_array, confusion_matrix_absicht_class, "Textklassifizierung-KI (Absicht)")
            neural_network.utils.show_conf_matrix(preds_szenario_array, loesung_szenario_array, confusion_matrix_szenario_class, "Textklassifizierung-KI (Szenario)")

            os.makedirs(os.path.dirname(config.TEXTKLASSIFIZIERUNG_TRAINED_PATH), exist_ok=True)
            torch.save(model.state_dict(), config.TEXTKLASSIFIZIERUNG_TRAINED_PATH)
            best_loss = val_loss
            best_epochs = epoch + 1
            print(f'Validation Loss: {best_loss}, neues Modell')
        else:
            print(f'Validation Loss: {val_loss}')
    
    end_zeit = time.time()

    trainingsdauer = (end_zeit - start_zeit) / 60

    print(f"\nTrainingsdauer: {trainingsdauer:.2f} Minuten")
    
    flat_preds_anmerkung_array = [item for sublist in best_preds_anmerkung_array for item in sublist]
    flat_loesung_anmerkung_array = [item for sublist in best_loesung_anmerkung_array for item in sublist]
    neural_network.utils.show_conf_matrix(flat_preds_anmerkung_array, flat_loesung_anmerkung_array, confusion_matrix_anmerkung_class, f"{best_epochs} Epochs | Total: {len(flat_preds_anmerkung_array)} | Textklassifizierung-KI (Anmerkung)", plot=True)
    neural_network.utils.show_conf_matrix(best_preds_absicht_array, best_loesung_absicht_array, confusion_matrix_absicht_class, f"{best_epochs} Epochs | Total: {len(best_preds_absicht_array)} | Textklassifizierung-KI (Absicht)", plot=True)
    neural_network.utils.show_conf_matrix(best_preds_szenario_array, best_loesung_szenario_array, confusion_matrix_szenario_class, f"{best_epochs} Epochs | Total: {len(best_preds_szenario_array)} | Textklassifizierung-KI (Szenario)", plot=True)

    absicht_szenario_label = []
    absicht_szenario_vorhersage = []
    absicht_szenario_loesung = []

    for i in range(len(best_preds_absicht_array)):
        pair_vorhersage = (int(best_preds_szenario_array[i]), int(best_preds_absicht_array[i]))
        pair_loesung = (int(best_loesung_szenario_array[i]), int(best_loesung_absicht_array[i]))

        if pair_vorhersage not in absicht_szenario_label:
            absicht_szenario_label.append(pair_vorhersage)
        if pair_loesung not in absicht_szenario_label:
            absicht_szenario_label.append(pair_loesung)

        index_vorhersage = absicht_szenario_label.index(pair_vorhersage)
        absicht_szenario_vorhersage.append(index_vorhersage)

        index_loesung = absicht_szenario_label.index(pair_loesung)
        absicht_szenario_loesung.append(index_loesung)

    absicht_szenario_label = [f"{presenter_textklassifizierung.such_szenario(encoder_szenario.classes_[szenario])} {presenter_textklassifizierung.such_absicht(encoder_absicht.classes_[absicht])}" for szenario, absicht in absicht_szenario_label]
    
    neural_network.utils.show_conf_matrix(absicht_szenario_vorhersage, absicht_szenario_loesung, absicht_szenario_label, f"{best_epochs} Epochs | Total: {len(absicht_szenario_vorhersage)} | Textklassifizierung-KI (Absicht + Szenario)", plot=True)

    anmerkung_absicht_szenario_label = []
    anmerkung_absicht_szenario_vorhersage = []
    anmerkung_absicht_szenario_loesung = []

    for i in range(len(best_preds_absicht_array)):
        for j in range(len(best_preds_anmerkung_array[i])):
            pair_vorhersage = (int(best_preds_anmerkung_array[i][j]), int(best_preds_szenario_array[i]), int(best_preds_absicht_array[i]))
            pair_loesung = (int(best_loesung_anmerkung_array[i][j]), int(best_loesung_szenario_array[i]), int(best_loesung_absicht_array[i]))

            if pair_vorhersage not in anmerkung_absicht_szenario_label:
                anmerkung_absicht_szenario_label.append(pair_vorhersage)
            if pair_loesung not in anmerkung_absicht_szenario_label:
                anmerkung_absicht_szenario_label.append(pair_loesung)

            index_vorhersage = anmerkung_absicht_szenario_label.index(pair_vorhersage)
            anmerkung_absicht_szenario_vorhersage.append(index_vorhersage)

            index_loesung = anmerkung_absicht_szenario_label.index(pair_loesung)
            anmerkung_absicht_szenario_loesung.append(index_loesung)

    anmerkung_absicht_szenario_label = [ (presenter_textklassifizierung.such_anmerkung(positive_anmerkung_class[anmerkung]), f"{presenter_textklassifizierung.such_szenario(encoder_szenario.classes_[szenario])} {presenter_textklassifizierung.such_absicht(encoder_absicht.classes_[absicht])}") for anmerkung, szenario, absicht in anmerkung_absicht_szenario_label]
    neural_network.utils.show_conf_matrix(anmerkung_absicht_szenario_vorhersage, anmerkung_absicht_szenario_loesung, anmerkung_absicht_szenario_label, f"{best_epochs} Epochs | Total: {len(anmerkung_absicht_szenario_vorhersage)} | Textklassifizierung-KI (Anmerkung + Absicht + Szenario)", plot=True)
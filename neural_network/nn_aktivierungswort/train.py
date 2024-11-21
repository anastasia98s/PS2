import os
import time
import torch
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split

import config
import neural_network.nn_aktivierungswort.utils
from neural_network.nn_aktivierungswort.model import Model
import neural_network.utils

def train():
    if not os.path.isfile(config.AKTIVIERUNGSWORT_DATENBANK_PATH):
        raise FileNotFoundError(f"\ndie Datenbank ist leer")
    merkmale, labels = neural_network.nn_aktivierungswort.utils.get_data(config.AKTIVIERUNGSWORT_DATENBANK_PATH)

    if len(merkmale > 1):
        train_merkmale, val_merkmale, train_labels, val_labels = train_test_split(merkmale, labels, test_size=0.2, random_state=42) #stratify=labels

        train_dataset = neural_network.nn_aktivierungswort.utils.MerkmaleDataset(train_merkmale, train_labels)
        train_data_loader = DataLoader( train_dataset,
                                        batch_size=config.AKTIVIERUNGSWORT_TRAIN_BATCH_SIZE,
                                        shuffle=True,
                                        pin_memory=True)
        
        val_dataset = neural_network.nn_aktivierungswort.utils.MerkmaleDataset(val_merkmale, val_labels)
        val_data_loader = DataLoader(   val_dataset,
                                        batch_size=config.AKTIVIERUNGSWORT_VALIDATION_BATCH_SIZE,
                                        shuffle=False,
                                        pin_memory=True)
        
        device = config.DEVICE 
        model = Model(config.AKTIVIERUNGSWORT_HIDDEN_UNITS_1, config.AKTIVIERUNGSWORT_HIDDEN_UNITS_2)
        model.to(device)

        print(len(train_merkmale), len(val_merkmale), len(train_labels), len(val_labels))

        if config.AKTIVIERUNGSWORT_RETRAIN_MODEL:
            try:
                model.load_state_dict(torch.load(config.AKTIVIERUNGSWORT_TRAINED_PATH, map_location=torch.device(config.DEVICE)))
                print("\n!!!Retraining!!!")
            except Exception as e:
                print(f"\nFehler beim Laden des Modells für das Retraining: {e}")

        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        start_zeit = time.time()

        best_loss = float('inf')
        best_preds_aktivierung_array = []
        best_loesung_aktivierung_array = []

        confusion_matrix_class = ["kein Aktivierungswort", "Aktivierungswort"]

        print("=" * 10)
        print("Device: " + str(device))
        print(f'Training Data: {len(train_merkmale)}')
        print(f'Validation Data: {len(val_merkmale)}')
        print(f'Total Data: {len(merkmale)}')

        for epoch in range(config.AKTIVIERUNGSWORT_EPOCHS):
            train_loss = neural_network.nn_aktivierungswort.utils.train_fn(train_data_loader, model, optimizer, device)
            val_loss, preds_aktivierung_array, loesung_aktivierung_array = neural_network.nn_aktivierungswort.utils.val_fn(val_data_loader, model, device)

            if val_loss < best_loss or epoch % 100 == 0 or epoch == config.AKTIVIERUNGSWORT_EPOCHS-1:
                best_preds_aktivierung_array = preds_aktivierung_array
                best_loesung_aktivierung_array = loesung_aktivierung_array
                neural_network.utils.show_conf_matrix(preds_aktivierung_array, loesung_aktivierung_array, confusion_matrix_class, "Aktivierung-KI", binary=True)
                print(f'\n== Epoch {epoch + 1}/{config.AKTIVIERUNGSWORT_EPOCHS}')
                print(f'Train Loss: {train_loss}')
                
                if val_loss < best_loss and config.AKTIVIERUNGSWORT_SAVE_MODEL:
                    os.makedirs(os.path.dirname(config.AKTIVIERUNGSWORT_TRAINED_PATH), exist_ok=True)
                    torch.save(model.state_dict(), config.AKTIVIERUNGSWORT_TRAINED_PATH)
                    best_loss = val_loss
                    print(f'Validation Loss: {best_loss}, neues Modell')
                else:
                    print(f'Validation Loss: {val_loss}')

        end_zeit = time.time()

        trainingsdauer = (end_zeit - start_zeit) / 60

        print(f"\nTrainingsdauer: {trainingsdauer:.2f} Minuten")

        neural_network.utils.show_conf_matrix(best_preds_aktivierung_array, best_loesung_aktivierung_array, confusion_matrix_class, f"Best {config.AKTIVIERUNGSWORT_EPOCHS} Epochs\nAktivierungsword-KI", binary=True, plot=True)
    else:
        print("\n!!!Zu wenige Daten, um Aktivierungswort-KI zu trainieren!!!")
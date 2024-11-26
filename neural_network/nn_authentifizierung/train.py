import os
import time
import joblib
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from utils.data_controller.user_controller.presenter import PresenterUser
import config
import neural_network.nn_authentifizierung.utils
from neural_network.nn_authentifizierung.model import Model

def train():
    if not os.path.isfile(config.USER_DATENBANK_PATH):
        raise FileNotFoundError(f"\ndie Datenbank ist leer")
    merkmale, benutzerids, encoder_benutzerids = neural_network.nn_authentifizierung.utils.get_data(config.USER_DATENBANK_PATH)
    if len(merkmale > 1):
        meta_data = {
            'encoder_benutzerids': encoder_benutzerids
        }
        joblib.dump(meta_data, config.AUTHENTIFIZIERUNG_META_PATH)
        
        train_merkmale, val_merkmale, train_benutzerids, val_benutzerids = train_test_split(merkmale, benutzerids, test_size=0.2, random_state=42) #stratify=benutzerids

        train_dataset = neural_network.nn_authentifizierung.utils.MerkmaleDataset(train_merkmale, train_benutzerids)
        train_data_loader = DataLoader( train_dataset,
                                        batch_size=config.AUTHENTIFIZIERUNG_TRAIN_BATCH_SIZE,
                                        shuffle=True,
                                        pin_memory=True)
        
        val_dataset = neural_network.nn_authentifizierung.utils.MerkmaleDataset(val_merkmale, val_benutzerids)
        val_data_loader = DataLoader(   val_dataset,
                                        batch_size=config.AUTHENTIFIZIERUNG_VALIDATION_BATCH_SIZE,
                                        shuffle=False,
                                        pin_memory=True)
        
        num_benutzerids = len(encoder_benutzerids.classes_)

        device = config.DEVICE 
        model = Model(num_benutzerids, config.AUTHENTIFIZIERUNG_HIDDEN_UNITS_1, config.AUTHENTIFIZIERUNG_HIDDEN_UNITS_2)
        model.to(device)

        if config.AUTHENTIFIZIERUNG_RETRAIN_MODEL:
            try:
                model.load_state_dict(torch.load(config.AUTHENTIFIZIERUNG_TRAINED_PATH, map_location=torch.device(config.DEVICE)))
                print("\n!!!Retraining!!!")
            except Exception as e:
                print(f"\nFehler beim Laden des Modells für das Retraining: {e}")

        optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=0.01)

        best_loss = float('inf')
        best_epochs = 1
        best_preds_authentifizierung_array = []
        best_loesung_authentifizierung_array = []

        confusion_matrix_class = []

        user_presenter = PresenterUser()
        for benutzerid in encoder_benutzerids.classes_:
            confusion_matrix_class.append(user_presenter.show_benutzer_name(benutzerid))

        print("=" * 10)
        print("Device: " + str(device))
        print(f'Training Data: {len(train_merkmale)}')
        print(f'Validation Data: {len(val_merkmale)}')
        print(f'Total Data: {len(merkmale)}')

        start_zeit = time.time()

        for epoch in range(config.AUTHENTIFIZIERUNG_EPOCHS):
            train_loss = neural_network.nn_authentifizierung.utils.train_fn(train_data_loader, model, optimizer, device)
            val_loss, preds_authentifizierung_array, loesung_authentifizierung_array = neural_network.nn_authentifizierung.utils.val_fn(val_data_loader, model, device)

            if val_loss < best_loss or epoch % 100 == 0 or epoch == config.AUTHENTIFIZIERUNG_EPOCHS-1:
                print(f'\n== Epoch {epoch + 1}/{config.AUTHENTIFIZIERUNG_EPOCHS}')
                print(f'Train Loss: {train_loss}')
                
                if val_loss < best_loss and config.AUTHENTIFIZIERUNG_SAVE_MODEL:
                    best_preds_authentifizierung_array = preds_authentifizierung_array
                    best_loesung_authentifizierung_array = loesung_authentifizierung_array
                    neural_network.utils.show_conf_matrix(preds_authentifizierung_array, loesung_authentifizierung_array, confusion_matrix_class, "Authentifizierung-KI")
                    os.makedirs(os.path.dirname(config.AUTHENTIFIZIERUNG_TRAINED_PATH), exist_ok=True)
                    torch.save(model.state_dict(), config.AUTHENTIFIZIERUNG_TRAINED_PATH)
                    best_loss = val_loss
                    best_epochs = epoch + 1
                    print(f'Validation Loss: {best_loss}, neues Modell')
                else:
                    print(f'Validation Loss: {val_loss}')

        end_zeit = time.time()

        trainingsdauer = (end_zeit - start_zeit) / 60

        print(f"\nTrainingsdauer: {trainingsdauer:.2f} Minuten")

        neural_network.utils.show_conf_matrix(best_preds_authentifizierung_array, best_loesung_authentifizierung_array, confusion_matrix_class, f"{best_epochs} Epochs | Total: {len(best_preds_authentifizierung_array)} | Authentifizierung-KI", plot=config.AUTHENTIFIZIERUNG_PLOT_CONFUSION_MATRIX)
    else:
        print("\n !!!Zu wenige Daten, um Authentifizierungs-KI zu trainieren!!!")
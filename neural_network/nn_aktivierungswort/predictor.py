import torch
import neural_network.nn_aktivierungswort.utils
from neural_network.nn_aktivierungswort.model import Model
import config
import os

class Predictor:
    def __init__(self, model_path):
        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"\n\n!!!Sie müssen Aktivierungswort-KI auf main.py trainieren!!!")
        self.device = config.DEVICE
        
        self.model = Model(config.AKTIVIERUNGSWORT_HIDDEN_UNITS_1, config.AKTIVIERUNGSWORT_HIDDEN_UNITS_2)
        self.model.load_state_dict(torch.load(model_path, weights_only=True, map_location=torch.device(config.DEVICE)))
        self.model.to(self.device).eval()
    
    def merkmale_prediction(self, mel_tensor):
        with torch.no_grad():
            label_lg = self.model(mel_tensor)
        return label_lg
    
    def label_extraction(self, label_lg):
        print("\nAktivierungswortwahrscheinlichkeit: " + str(label_lg.item()) + "/" + str(config.AKTIVIERUNGSWORT_NOTEN))
        predicted_label = None
        #print(torch.round(label_lg))
        if label_lg.item() > config.AKTIVIERUNGSWORT_NOTEN:
            predicted_label = 1
        else:
            predicted_label = 0
        return predicted_label
                
    def predict(self, merkmale_data):
        merkmale_features = neural_network.nn_aktivierungswort.utils.extract_features(merkmale_data, config.AUDIO_SAMPLE_RATE)
        mel_tensor = torch.tensor(merkmale_features, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(self.device)
        label_lg = self.merkmale_prediction(mel_tensor)
        return self.label_extraction(label_lg)
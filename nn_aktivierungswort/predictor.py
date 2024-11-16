import torch
import nn_aktivierungswort.utils
from nn_aktivierungswort.model import Model
import config
import os

class Predictor:
    def __init__(self, model_path):
        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"\nSie müssen Aktivierungswort-KI auf main.py trainieren")
        self.device = config.DEVICE
        
        self.model = Model(config.AKTIVIERUNGSWORT_HIDDEN_UNITS_1, config.AKTIVIERUNGSWORT_HIDDEN_UNITS_2)
        self.model.load_state_dict(torch.load(model_path, weights_only=True))
        self.model.to(self.device).eval()
    
    def merkmale_prediction(self, mfcc_tensor):
        with torch.no_grad():
            label_lg = self.model(mfcc_tensor)
        return label_lg
    
    def label_extraction(self, label_lg):
        #probabilities = torch.sigmoid(label_lg)
        
        print("Wahrscheinlichkeit: " + str(label_lg.item()))
        predicted_label = None
        if label_lg.item() > config.AKTIVIERUNGSWORT_NOTEN:
            predicted_label = 1
        else:
            predicted_label = 0
        return predicted_label
                
    def predict(self, merkmale_data):
        merkmale_features = nn_aktivierungswort.utils.extract_features(merkmale_data, config.AUDIO_SAMPLE_RATE)
        mfcc_tensor = torch.tensor(merkmale_features, dtype=torch.float32).unsqueeze(0).to(self.device)
        label_lg = self.merkmale_prediction(mfcc_tensor)
        return self.label_extraction(label_lg)
import joblib
import torch
import neural_network.nn_authentifizierung.utils
from neural_network.nn_authentifizierung.model import Model
import config
import os
import neural_network.utils

class Predictor:
    def __init__(self, model_path):
        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"\nSie müssen Authentifizierung-KI auf main.py trainieren")
        self.device = config.DEVICE
        self.meta_data = joblib.load(config.AUTHENTIFIZIERUNG_META_PATH)
        
        self.encoder_benutzerids = self.meta_data['encoder_benutzerids']
        
        self.num_benutzerids = len(self.encoder_benutzerids.classes_)

        self.model = Model(self.num_benutzerids, config.AUTHENTIFIZIERUNG_HIDDEN_UNITS_1, config.AUTHENTIFIZIERUNG_HIDDEN_UNITS_2)
        self.model.load_state_dict(torch.load(model_path, weights_only=True))
        self.model.to(self.device).eval()
    
    def merkmale_prediction(self, mfcc_tensor):
        with torch.no_grad():
            name_lg = self.model(mfcc_tensor)
        return name_lg
    
    def name_extraction(self, name_lg):
        class_scores, class_preds = neural_network.utils.to_yhat(name_lg)
        return class_preds, [self.encoder_benutzerids.classes_, class_scores[0]]
                
    def predict(self, merkmale_data):
        # merkmale_data = nn_authentifizierung.utils.record_voice(5, config.AUDIO_SAMPLE_RATE)
        merkmale_features = neural_network.nn_authentifizierung.utils.extract_features(merkmale_data, config.AUDIO_SAMPLE_RATE)
        mfcc_tensor = torch.FloatTensor(merkmale_features).unsqueeze(0).to(self.device)
        name_lg = self.merkmale_prediction(mfcc_tensor)
        return self.name_extraction(name_lg)
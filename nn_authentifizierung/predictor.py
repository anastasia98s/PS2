import joblib
import torch
import nn_authentifizierung.utils
from nn_authentifizierung.model import Model
import config
import numpy as np

class Predictor:
    def __init__(self, model_path):
        self.device = config.DEVICE
        self.meta_data = joblib.load(config.AUTHENTIFIZIERUNG_META_PATH)
        
        self.encoder_namen = self.meta_data['encoder_namen']
        
        self.num_namen = len(self.encoder_namen.classes_)

        self.model = Model(self.num_namen, config.AUTHENTIFIZIERUNG_HIDDEN_UNITS_1, config.AUTHENTIFIZIERUNG_HIDDEN_UNITS_2)
        self.model.load_state_dict(torch.load(model_path, weights_only=True))
        self.model.to(self.device).eval()

    @staticmethod
    def to_yhat(logits):
        logits = logits.view(-1, logits.shape[-1]).cpu().detach()
        probs = torch.softmax(logits, dim=1)
        y_hat = torch.argmax(probs, dim=1)
        return probs.numpy(), y_hat.numpy()
    
    def audio_prediction(self, mfcc_tensor):
        with torch.no_grad():
            name_lg = self.model(mfcc_tensor)
        return name_lg
    
    def name_extraction(self, name_lg):
        class_scores, class_preds = self.to_yhat(name_lg)
        return class_preds, [self.encoder_namen.classes_, class_scores[0]]
                
    def predict(self, audio_data):
        # audio_data = nn_authentifizierung.utils.record_voice(5, config.AUTHENTIFIZIERUNG_SAMPLE_RATE)
        audio_features = nn_authentifizierung.utils.extract_features(audio_data, config.AUTHENTIFIZIERUNG_SAMPLE_RATE)
        mfcc_tensor = torch.FloatTensor(audio_features).unsqueeze(0).to(self.device)
        name_lg = self.audio_prediction(mfcc_tensor)
        return self.name_extraction(name_lg)
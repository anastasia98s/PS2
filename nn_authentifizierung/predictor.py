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
                
    def predict(self):
        audio_data = nn_authentifizierung.utils.record_voice(duration=3)
        mfcc_features = nn_authentifizierung.utils.extract_features(audio_data)
        name_scores_dict = {}
        for feature in mfcc_features.T:
            mfcc_tensor = torch.FloatTensor(feature).unsqueeze(0).to(self.device)
            name_lg = self.audio_prediction(mfcc_tensor)
            index, name_score_array = self.name_extraction(name_lg)
            
            class_name = name_score_array[0][index]
            class_score = name_score_array[1][index]

            if isinstance(class_name, np.ndarray):
                class_name = class_name.item()
            if class_name in name_scores_dict:
                name_scores_dict[class_name].append(class_score)
            else:
                name_scores_dict[class_name] = [class_score]

            #print(f"Name: {class_name}, Score: {class_score}")

        avg_scores = {name: sum(scores)/len(scores) for name, scores in name_scores_dict.items()}
        best_name = max(avg_scores, key=avg_scores.get)
        best_score = avg_scores[best_name]
        return best_name, best_score
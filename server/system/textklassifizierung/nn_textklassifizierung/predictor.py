import api
import joblib
import torch
from nn_textklassifizierung.model import Model
import config
import os
from nn_textklassifizierung import train
import nn_textklassifizierung.utils

class Predictor:
    def __init__(self, model_path):
        if not os.path.isfile(model_path):
            train.train()
            # raise FileNotFoundError(f"\nSie müssen Textklassifizierung-KI auf main.py trainieren")
        self.tokenizer = config.TEXTKLASSIFIZIERUNG_TOKENIZER
        self.max_len = config.TEXTKLASSIFIZIERUNG_MAX_LEN
        self.device = config.DEVICE
        
        self.meta_data = joblib.load(config.TEXTKLASSIFIZIERUNG_META_PATH)
        
        self.encoder_anmerkung = self.meta_data['encoder_anmerkung']
        self.encoder_absicht = self.meta_data['encoder_absicht']
        self.encoder_szenario = self.meta_data['encoder_szenario']
        
        self.num_anmerkung = len(self.encoder_anmerkung.classes_)
        self.num_absicht = len(self.encoder_absicht.classes_)
        self.num_szenario = len(self.encoder_szenario.classes_)

        self.model = Model(self.num_anmerkung, self.num_absicht, self.num_szenario)
        self.model.load_state_dict(torch.load(model_path, weights_only=True, map_location=torch.device(config.DEVICE)))
        self.model.to(self.device).eval()

    def process_satz(self, satz):
        satz = str(satz)
        woerter = " ".join(satz.split()).split()

        tokenized_ids = []
        woerter_data_array = []

        for wort in woerter:
            token_ids = self.tokenizer.encode(wort, add_special_tokens=False)
            token_len = len(token_ids)
            tokenized_ids.extend(token_ids)
            woerter_data_array.append((wort, token_len))
        
        tokenized_ids = tokenized_ids[:self.max_len-2]
        tokenized_ids = [101] + tokenized_ids + [102]
        mask, token_type_ids = [1]*len(tokenized_ids), [0]*len(tokenized_ids)

        padding_len = self.max_len - len(tokenized_ids)
        ids = tokenized_ids + ([0] * padding_len)
        mask = mask + ([0] * padding_len)
        token_type_ids = token_type_ids + ([0] * padding_len)
        
        ids = torch.tensor(ids,dtype=torch.long).unsqueeze(0).to(self.device)
        mask = torch.tensor(mask, dtype=torch.long).unsqueeze(0).to(self.device)
        token_type_ids = torch.tensor(token_type_ids, dtype=torch.long).unsqueeze(0).to(self.device)

        return ids, mask, token_type_ids, tokenized_ids, woerter_data_array
    
    def satz_prediction(self, ids, mask, token_type_ids):
        with torch.no_grad():
            anmerkung_lg,absicht_lg,szenario_lg  = self.model(ids,mask,token_type_ids)
        return anmerkung_lg, absicht_lg, szenario_lg
        
    def anmerkung_extraction(self, anmerkung_lg, tokenized_ids, woerter_data_array):
        anmerkung_scores, anmerkung_preds = nn_textklassifizierung.utils.to_yhat(anmerkung_lg)
        anmerkung_scores = anmerkung_scores[1:len(tokenized_ids)-1, :]

        anmerkung_indexs = anmerkung_preds[1:len(tokenized_ids)-1]

        trim_anmerkung_indexs = []
        trim_anmerkung_scores = []
        trim_index = 0
        for wort_data in woerter_data_array:
            _, wort_len = wort_data

            trim_anmerkung_indexs.append(anmerkung_indexs[trim_index])
            trim_anmerkung_scores.append(anmerkung_scores[trim_index])
            trim_index += wort_len

        return trim_anmerkung_indexs, trim_anmerkung_scores
        
    def classification(self, logits, typ='absicht'):

        if typ == 'absicht':
            enc = self.encoder_absicht
        else:
            enc = self.encoder_szenario

        class_scores, class_preds = nn_textklassifizierung.utils.to_yhat(logits)

        return class_preds, [enc.classes_, class_scores[0]]
    
    def predict(self, satz):
        
        ids, mask, token_type_ids, tokenized_ids, woerter_data_array = self.process_satz(satz)

        anmerkung_lg, absicht_lg, szenario_lg = self.satz_prediction(ids, mask, token_type_ids)

        anmerkung_indexs, anmerkung_scores = self.anmerkung_extraction(anmerkung_lg, tokenized_ids, woerter_data_array)

        absicht_label_index, absichten_class_scores = self.classification(absicht_lg, typ='absicht')
        szenario_label_index, szenarios_class_scores = self.classification(szenario_lg, typ='szenario')

        woerter_array = [wort for wort, _ in woerter_data_array]
        return (self.encoder_anmerkung.classes_,
                [anmerkung_indexs, woerter_array, anmerkung_scores],
                absicht_label_index[0],
                absichten_class_scores,
                szenario_label_index[0],
                szenarios_class_scores)
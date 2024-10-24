import joblib
import torch
from nn_textklassifizierung.model import Model
import config

class Predictor:
    def __init__(self, model_path):
        
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
        self.model.load_state_dict(torch.load(model_path, weights_only=True))
        self.model.to(self.device).eval()

    @staticmethod
    def to_yhat(logits):
        logits = logits.view(-1, logits.shape[-1]).cpu().detach()
        probs = torch.softmax(logits, dim=1)
        y_hat = torch.argmax(probs, dim=1)
        return probs.numpy(), y_hat.numpy()

    def process_satz(self,satz):
        satz = str(satz)
        satz = " ".join(satz.split())
        inputs = self.tokenizer.encode_plus(
            satz,
            None,
            add_special_tokens=True,
            truncation=True,
            max_length = self.max_len
        )
        
        tokenized_ids = inputs['input_ids']
        mask = inputs['attention_mask']
        token_type_ids = inputs['token_type_ids']
        wort_pieces = self.tokenizer.decode(inputs['input_ids']).split()[1:-1]

        padding_len = self.max_len - len(tokenized_ids)
            
        ids = tokenized_ids + ([0] * padding_len)
        mask = mask + ([0] * padding_len)
        token_type_ids = token_type_ids + ([0] * padding_len)
        
        ids = torch.tensor(ids,dtype=torch.long).unsqueeze(0).to(self.device)
        mask = torch.tensor(mask, dtype=torch.long).unsqueeze(0).to(self.device)
        token_type_ids = torch.tensor(token_type_ids, dtype=torch.long).unsqueeze(0).to(self.device)
        return ids, mask, token_type_ids, tokenized_ids, wort_pieces
    
    def satz_prediction(self, ids, mask, token_type_ids):
        with torch.no_grad():
            anmerkung_lg,absicht_lg,szenario_lg  = self.model(ids,mask,token_type_ids)
        return anmerkung_lg, absicht_lg, szenario_lg
        
    def anmerkung_extraction(self, anmerkung_lg, tokenized_ids, wort_pieces):
        anmerkung_scores, anmerkung_preds = self.to_yhat(anmerkung_lg)
        anmerkung_scores = anmerkung_scores[1:len(tokenized_ids)-1, :]

        anmerkung_indexs = anmerkung_preds[1:len(tokenized_ids)-1]
        len_wort = len(wort_pieces)

        anmerkung_indexs = anmerkung_indexs[:len_wort]
        anmerkung_scores = anmerkung_scores[:len_wort]

        return anmerkung_indexs, anmerkung_scores
        
    def classification(self, logits, typ='absicht'):

        if typ == 'absicht':
            enc = self.encoder_absicht
        else:
            enc = self.encoder_szenario

        class_scores, class_preds = self.to_yhat(logits)

        return class_preds, [enc.classes_, class_scores[0]]
    
    def predict(self, satz):
        
        ids,mask, token_type_ids, tokenized_ids, wort_pieces = self.process_satz(satz)

        anmerkung_lg, absicht_lg, szenario_lg = self.satz_prediction(ids,mask,token_type_ids)

        anmerkung_indexs, anmerkung_scores = self.anmerkung_extraction(anmerkung_lg, tokenized_ids, wort_pieces)

        absicht_label_index, absichten_class_scores = self.classification(absicht_lg, typ='absicht')
        szenario_label_index, szenarios_class_scores = self.classification(szenario_lg, typ='szenario')
             
        return (self.encoder_anmerkung.classes_,
                [anmerkung_indexs, wort_pieces, anmerkung_scores],
                absicht_label_index[0],
                absichten_class_scores,
                szenario_label_index[0],
                szenarios_class_scores)
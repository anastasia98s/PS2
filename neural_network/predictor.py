import joblib
import torch
from neural_network.model import Model
import config

class Predictor:
    def __init__(self, model_path):
        
        self.tokenizer = config.TOKENIZER
        self.max_len = config.MAX_LEN
        self.device = config.DEVICE
        
        self.meta_data = joblib.load(config.META_PATH)
        
        self.enc_anmerkung = self.meta_data['enc_anmerkung']
        self.enc_absicht = self.meta_data['enc_absicht']
        self.enc_szenario = self.meta_data['enc_szenario']
        
        self.num_anmerkung = len(self.enc_anmerkung.classes_)
        self.num_absicht = len(self.enc_absicht.classes_)
        self.num_szenario = len(self.enc_szenario.classes_)

        self.model = Model(self.num_anmerkung, self.num_absicht, self.num_szenario)
        self.model.load_state_dict(torch.load(model_path))
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
        return ids,mask,token_type_ids,tokenized_ids,wort_pieces
    
    def satz_prediction(self,ids,mask,token_type_ids):
        anmerkung_hs,absicht_hs,szenario_hs  = self.model(ids,mask,token_type_ids)
        return anmerkung_hs,absicht_hs,szenario_hs   
    
    @staticmethod
    def woerter_to_labels_json(word_pieces,labels):
        return {w:l for w,l in zip(word_pieces,labels)}

    @staticmethod
    def woerter_to_scores_json(words_pieces, scores):
        return {w:cs for w,cs in zip(words_pieces, scores)}
    
    def anmerkung_extraction(self, anmerkung_hs, tokenized_ids, wort_pieces):
        anmerkung_scores, anmerkung_preds = self.to_yhat(anmerkung_hs)
        anmerkung_scores = anmerkung_scores[1:len(tokenized_ids)-1, :]

        anmerkung_labels = self.enc_anmerkung.inverse_transform(anmerkung_preds)[1:len(tokenized_ids)-1]
        # woerter_labels_json = self.woerter_to_labels_json(wort_pieces, anmerkung_labels)
        # woerter_scores_json = self.woerter_to_scores_json(wort_pieces, anmerkung_scores)

        # print("\n\n",anmerkung_scores, "\n\n")
        # print(self.woerter_to_labels_json(wort_pieces, anmerkung_labels))
        # print("\n\n", self.woerter_to_scores_json(wort_pieces, anmerkung_scores), "\n\n")

        anmerkung_indexs = anmerkung_preds[1:len(tokenized_ids)-1]
        len_wort = len(wort_pieces)

        """ print("\n\n\n", wort_pieces, "\n\n\n")
        print("\n all class", self.enc_anmerkung.classes_, "\n")

        print("\n index class", anmerkung_indexs[:len_wort], "\n")
        print("\n score", anmerkung_scores[:len_wort], "\n") """

        anmerkung_indexs = anmerkung_indexs[:len_wort]
        anmerkung_scores = anmerkung_scores[:len_wort]

        # print("\n\n",anmerkung_scores, "\n\n")

        # print(len(anmerkung_indexs), len(anmerkung_indexs), len(wort_pieces))

        return anmerkung_indexs, anmerkung_scores
        
    def classification(self, logits, typ='absicht'):

        if typ == 'absicht':
            enc = self.enc_absicht
        else:
            enc = self.enc_szenario

        class_scores, class_preds = self.to_yhat(logits)

        # satz_labels_json = self.satz_to_labels_json(enc.inverse_transform(class_preds), len(class_preds))
        # class_scores_json = self.classes_to_scores_json(enc.classes_, class_scores)

        # enc.inverse_transform(class_preds)

        return class_preds, [enc.classes_, class_scores[0]]
    
    def predict(self, satz):
        
        ids,mask, token_type_ids, tokenized_ids, wort_pieces = self.process_satz(satz)

        anmerkung_hs, absicht_hs, szenario_hs = self.satz_prediction(ids,mask,token_type_ids)

        anmerkung_indexs, anmerkung_scores = self.anmerkung_extraction(anmerkung_hs, tokenized_ids, wort_pieces)

        absicht_label_index, absichten_class_scores = self.classification(absicht_hs, typ='absicht')
        szenario_label_index, szenarios_class_scores = self.classification(szenario_hs, typ='szenario')
             
        return (self.enc_anmerkung.classes_,
                [anmerkung_indexs, wort_pieces, anmerkung_scores],
                absicht_label_index[0],
                absichten_class_scores,
                szenario_label_index[0],
                szenarios_class_scores)
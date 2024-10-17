import torch
import config
class IntentScenarioDataset:
    def __init__(self,text,absicht,szenario):
        self.texts = text 
        self.absicht = absicht
        self.szenario = szenario

        self.tokenizer = config.TOKENIZER
        self.max_len = config.MAX_LEN
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self,item):
        absicht = self.absicht[item]
        szenario = self.szenario[item]

        return {
            'target_absicht': torch.tensor(absicht,dtype=torch.long),
            'target_szenario': torch.tensor(szenario,dtype=torch.long)
        }
            
            
class EntityDataset:
    def __init__(self, text, anmerkung):
        self.texts = text
        self.anmerkung = anmerkung
        self.tokenizer = config.TOKENIZER
        self.max_len = config.MAX_LEN 
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self,item):
        text = self.texts[item]
        anmerkung = self.anmerkung[item]

        ids = []
        target_anmerkung = []
        for i,wort in enumerate(text):
            token_ids = self.tokenizer.encode(wort, add_special_tokens=False)
            wort_piece_anmerkung = [anmerkung[i]] * len(token_ids)

            ids.extend(token_ids)
            target_anmerkung.extend(wort_piece_anmerkung)

        ids = ids[:self.max_len-2]
        target_anmerkung = target_anmerkung[:self.max_len-2]

        ids = [101] + ids + [102]
        target_anmerkung = [0] + target_anmerkung + [0]
        
        mask, token_type_id = [1]*len(ids), [0]*len(ids)

        padding_len = self.max_len - len(ids)
        
        ids = ids + ([0] * padding_len)
        target_anmerkung = target_anmerkung + ([0] * padding_len)
        mask = mask + ([0] * padding_len)
        token_type_id = token_type_id + ([0] * padding_len)

        return {
            'ids': torch.tensor(ids,dtype=torch.long),
            'target_anmerkung': torch.tensor(target_anmerkung,dtype=torch.long),
            'mask': torch.tensor(mask,dtype=torch.long),
            'token_type_ids': torch.tensor(token_type_id,dtype=torch.long)
        }

class NLUDataset(torch.utils.data.Dataset):

    def __init__(self, text, anmerkung, absicht, szenario):
        self.texts = text
        self.anmerkung = anmerkung
        self.absicht = absicht
        self.szenario = szenario

        self.anmerkung_dataset = EntityDataset(self.texts,
                                            self.anmerkung)
        self.absicht_szenario_dataset = IntentScenarioDataset(
                                                                self.texts,
                                                                self.absicht,
                                                                self.szenario
                                                            )
    def __len__(self):
        return len(self.texts)

    def __getitem__(self,item):
        anmerkung_item = self.anmerkung_dataset[item] 
        absicht_szenario_item = self.absicht_szenario_dataset[item]
        
        return {
            'ids':anmerkung_item['ids'],
            'target_anmerkung': anmerkung_item['target_anmerkung'],
            'target_absicht': absicht_szenario_item['target_absicht'],
            'target_szenario':absicht_szenario_item['target_szenario'],
            'mask': anmerkung_item['mask'],
            'token_type_ids': anmerkung_item['token_type_ids'],
        }
        
        















        
if __name__ == "__main__":
    test_text = [['hello','siri', 'stop']]
    test_anmerkung = [[3, 1, 5]]
    test_absicht, test_szenario = [[[3]],[2]]

    #test er dataset 
    er_dataset = EntityDataset(
                                text=test_text,
                                anmerkung=test_anmerkung
                            )
    out = er_dataset[0]

    # print("Entity Dataset Output:", out)
    
    is_dataset = IntentScenarioDataset(test_text,test_absicht, test_anmerkung)
    out = is_dataset[0]

    print("Intent Scenario Dataset Output (require_text=False):", out)

    #test NLU wrapper dataset 
    sp_dataset = NLUDataset(
                                test_text,
                                test_anmerkung,
                                test_absicht,
                                test_szenario
                            )
    out = sp_dataset[0]

    # print("NLU Dataset Output:", out)



                
        

        

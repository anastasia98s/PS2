import torch.nn as nn
import transformers
import config 
class Model(nn.Module):
    def __init__(self, num_anmerkung, num_absicht, num_szenario):
        super(Model, self).__init__()
        
        self.num_anmerkung = num_anmerkung
        self.num_absicht = num_absicht
        self.num_szenario = num_szenario

        self.bert = transformers.BertModel.from_pretrained(
            config.BASE_MODEL
        )

        self.drop_1 = nn.Dropout(0.3)
        self.drop_2 = nn.Dropout(0.3)
        self.drop_3 = nn.Dropout(0.3)

        self.out_anmerkung = nn.Linear(768, self.num_anmerkung)
        self.out_absicht = nn.Linear(768, self.num_absicht)
        self.out_szenario = nn.Linear(768, self.num_szenario)

    def forward(self, ids,mask,token_type_ids):

        out = self.bert(
                        input_ids=ids,
                        attention_mask=mask,
                        token_type_ids=token_type_ids
                    )
        hs, cls_hs = out['last_hidden_state'], out['pooler_output']
        anmerkung_hs = self.drop_1(hs)
        absicht_hs = self.drop_2(cls_hs)
        szenario_hs = self.drop_3(cls_hs)

        anmerkung_hs = self.out_anmerkung(anmerkung_hs)
        absicht_hs = self.out_absicht(absicht_hs)
        szenario_hs = self.out_szenario(szenario_hs)

        return anmerkung_hs,absicht_hs,szenario_hs
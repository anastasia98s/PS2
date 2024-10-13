import torch
import torch.nn as nn
import json
import numpy as np
from pathlib import Path

gl_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class DialogModel(nn.Module):
    def __init__(self, input_size, hidden_1_size, hidden_2_size, hidden_3_size, num_classes):
        super(DialogModel, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_1_size) 
        self.l2 = nn.Linear(hidden_1_size, hidden_2_size)
        self.l3 = nn.Linear(hidden_2_size, hidden_3_size) 
        self.l4 = nn.Linear(hidden_3_size, num_classes) 
        self.relu = nn.ReLU()
    
    def forward(self, x):
        result = self.l1(x)
        result = self.relu(result)
        result = self.l2(result)
        result = self.relu(result)
        result = self.l3(result)
        result = self.relu(result)
        result = self.l4(result)
        return result
    

with open('assets/data.json', 'r', encoding='utf-8') as f:
    daten = json.load(f)



import nltk
# nltk.download('punkt')
# from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("german") #PorterStemmer()

from nltk.corpus import stopwords
# nltk.download('stopwords')

from nltk.stem import WordNetLemmatizer
# nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

def tokenisierer(satz):
    tokenizer = nltk.RegexpTokenizer(r'\[.*?\]|\w+|\$[\d\.]+|\S+')
    return tokenizer.tokenize(satz)

def lemmatisierer(wort):
    if wort.startswith('[') and wort.endswith(']'):
        return wort
    return lemmatizer.lemmatize(wort) #stemmer.stem(word.lower())

def stemming(wort):
    if wort.startswith('[') and wort.endswith(']'):
        return wort
    return stemmer.stem(wort.lower()) #stemmer.stem(word.lower())

def parameter_encoder(wort):
    if any(wort.lower() == datum_einheit.lower() for datum_einheit in daten["data_datum_einheit"]):
        return "[DATUM_EINHEIT]", 1
    elif any(wort.lower() == ort.lower() for ort in daten["data_ort"]):
        return "[ORT]", 2
    elif any(stemming(wort) == stemming(zeit_einheit) for zeit_einheit in daten["data_zeit_einheit"]):
        return "[ZEIT_EINHEIT]", 3
    elif wort.lstrip('-').replace('.', '', 1).replace(',', '', 1).isdigit(): # elif wort.isdigit() or (wort.replace('.', '', 1).isdigit() and wort.count('.') < 2):
        return "[NUMMER]", 4
    else:
        return wort, 0

def stopp_woerter(sprache):
    stopp_extra = ["'s", "?", ".", "!"]
    return stopwords.words(sprache) + stopp_extra


def satz_entcoder(tokenisierter_satz, woerter):
    satzwoerter = [lemmatisierer(stemming(wort)) for wort in tokenisierter_satz]
    entcode_array = np.zeros(len(woerter), dtype=np.float32)
    for idx, w in enumerate(woerter):
        if w in satzwoerter: 
            entcode_array[idx] = 1

    return entcode_array

MODEL_PATH = Path("assets")
MODEL_PATH.mkdir(parents=True, exist_ok=True)
MODEL_NAME = "data.pth"
MODEL_SAVE_PATH = MODEL_PATH / MODEL_NAME
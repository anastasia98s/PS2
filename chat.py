import random
from datetime import datetime
import wikipedia
import re
import requests

import torch

from global_dialog import DialogModel, daten, gl_device, tokenisierer, satz_entcoder, parameter_encoder, MODEL_SAVE_PATH

trained_data = torch.load(MODEL_SAVE_PATH)

h_input_size = trained_data["input_size"]
h_hidden_layer_1_size = trained_data["hidden_1_size"]
h_hidden_layer_2_size = trained_data["hidden_2_size"]
h_hidden_layer_3_size = trained_data["hidden_3_size"]
h_output_size = trained_data["output_size"]
g_woerter = trained_data["woerter"]
g_kategorien = trained_data['kategorien']
model_state = trained_data["model_state"]

model = DialogModel(h_input_size, h_hidden_layer_1_size, h_hidden_layer_2_size, h_hidden_layer_3_size, h_output_size).to(gl_device)
print(h_hidden_layer_2_size)
model.load_state_dict(model_state)
model.eval()

wikipedia.set_lang("de")
bot_name = "Assistent"
user_input = None
user_name = "User"
user_datum_einheit = "Heute"
user_ort = "Dresden"
user_zeit_einheit = "Minuten"
user_nummer = "..."
user_wikipedia = "hmm..."
user_datum = datetime.now().strftime("%d.%m.%Y")
user_zeit = datetime.now().strftime("%H:%M")
print("=> zum Beenden 'quit' eingeben")

def fetch_wikipedia():
    return wikipedia.summary(user_input, sentences=5)

def fetch_wetter():
    url = f"http://wttr.in/{user_ort}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return "..."

pattern_fn = r"%%(.*?)%%"

while True:
    user_input = input("Du: ")
    
    if user_input == "quit":
        break

    sentence = tokenisierer(user_input)

    tmp_sentence = []
    for wort in sentence:
        result_wort, result_typ = parameter_encoder(wort)
        tmp_sentence.append(result_wort)

        if result_typ == 1:
            user_datum_einheit = wort
        elif result_typ == 2:
            user_ort = wort.capitalize()
        elif result_typ == 3:
            user_zeit_einheit = wort
        elif result_typ == 4:
            user_nummer = wort

    sentence = tmp_sentence
    
    X = satz_entcoder(sentence, g_woerter)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(gl_device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    kategorie = g_kategorien[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for dialog in daten['data_dialoge']['dialoge']:
            if kategorie == dialog["kategorie"]:
                antwort_dialog = random.choice(dialog['antwort'])

                matches_fn = re.findall(pattern_fn, antwort_dialog)

                for function_name in matches_fn:
                    result_fn = globals()[function_name]()
                    antwort_dialog = antwort_dialog.replace(f"%%{function_name}%%", result_fn)

                print(f"{bot_name}: {antwort_dialog
                                     .format(name=user_name,
                                             datum_einheit=user_datum_einheit,
                                             ort=user_ort,
                                             datum=user_datum,
                                             zeit=user_zeit,
                                             zeit_einheit=user_zeit_einheit,
                                             nummer=user_nummer,
                                             wikipedia=user_wikipedia)}")
    else:
        print(f"{bot_name}: Ich verstehe nicht...")
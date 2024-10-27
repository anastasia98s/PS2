import webview

from data.data_controller.model import Model
from data.data_controller.view import View
from data.data_controller.presenter import Presenter

from utils.audio import Audio
from nn_textklassifizierung.predictor import Predictor as PredictorText
from nn_textklassifizierung import train as train_text
from nn_authentifizierung import train as train_audio
from nn_authentifizierung.predictor import Predictor as PredictorUser
import config

def main():
    audio = Audio()
    predictor_text = PredictorText(config.TEXTKLASSIFIZIERUNG_TRAINED_PATH)
    predictor_user = PredictorUser(config.AUTHENTIFIZIERUNG_TRAINED_PATH)
    while True:
        print("\nBitte wähle eine Option:")
        print("1. AI Textklassifizierung")
        print("2. AI Authentifizierung")
        print("3. Predict All")
        print("4. Beenden")
        auswahl = input("Gib die Nummer der Option ein: ")
        if auswahl == '1':
            while True:
                print("\n==Textklassifizierung")
                print("Bitte wähle eine Option:")
                print("1. Datenkontrolle")
                print("2. AI Training")
                print("3. Predict")
                print("4. züruck")
                
                auswahl = input("Gib die Nummer der Option ein: ")

                if auswahl == '1':
                    model = Model()
                    view = View()
                    presenter = Presenter(model, view)

                    webview.create_window('Data Controller', html=view.showPage(1), js_api=presenter)
                    webview.start()
                elif auswahl == '2':
                    train_text.train()
                elif auswahl == '3':
                    print("„quit“ zum Beenden\n")
                    while True:

                        text = input("Satz: ")
                        if text == "quit":
                            break

                        (
                            anmerkung_satz_labels,
                            woerter_anmerkungen,
                            absicht_satz_labels,
                            absicht_class_scores,
                            szenario_satz_labels,
                            szenario_class_scores) = predictor_text.predict(text)
                        
                        print("\n\n" + "=" * 30)
                        satz_length = len(woerter_anmerkungen[0])
                        for i in range(satz_length):
                            print(f"{woerter_anmerkungen[1][i]} = {anmerkung_satz_labels[woerter_anmerkungen[0][i]]} = {woerter_anmerkungen[2][i][woerter_anmerkungen[0][i]] * 100}%")
                        print("=" * 30)
                        print(f"absicht = {absicht_class_scores[0][absicht_satz_labels]} = {absicht_class_scores[1][absicht_satz_labels] * 100}%")
                        print("=" * 30)
                        print(f"szenario = {szenario_class_scores[0][szenario_satz_labels]} = {szenario_class_scores[1][szenario_satz_labels] * 100}%")
                        print("=" * 30 + "\n\n")
                elif auswahl == '4':
                    break
                else:
                    print("Ungültige Auswahl, bitte versuche es erneut.")
        elif auswahl == '2':
            while True:
                print("\n==Authentifizierung")
                print("Bitte wähle eine Option:")
                print("1. Data Input")
                print("2. AI Training")
                print("3. Predict")
                print("4. züruck")
                auswahl = input("Gib die Nummer der Option ein: ")
                if auswahl == '1':
                    import nn_authentifizierung.utils
                    name = input("Name: ")

                    print("\nnein, gut, schlecht, danke, bitte, heute, morgen, jetzt, warum, weil, immer, nie, manchmal, oft, vielleicht, gern, richtig, falsch, groß, klein, schnell, langsam, hoch, niedrig, alt, jung, neu, alt, hell, dunkel, kalt, warm, heiß, schön, hässlich\n")
                    
                    voice_data = audio.listen(5, config.AUTHENTIFIZIERUNG_SAMPLE_RATE)
                    
                    antwort = input("speichern? j/n = ")
                    if antwort == 'j':
                        features = nn_authentifizierung.utils.extract_features(voice_data, config.AUTHENTIFIZIERUNG_SAMPLE_RATE)
                        nn_authentifizierung.utils.save_features_to_csv(config.AUTHENTIFIZIERUNG_DATASET_PATH, features, name)
                if auswahl == '2':
                    train_audio.train()
                if auswahl == '3':
                    signal = audio.listen(5, config.AUTHENTIFIZIERUNG_SAMPLE_RATE)
                    name_indexs, name_label_scores = predictor_user.predict(signal)
                    print("\n" + "=" * 30)
                    print(f"Name = {name_label_scores[0][name_indexs].item()} = {name_label_scores[1][name_indexs].item() * 100}%")
                    print("=" * 30 + "\n")
                if auswahl == '4':
                    break
        elif auswahl == '3':
            signal = audio.listen(5, config.AUTHENTIFIZIERUNG_SAMPLE_RATE)
            text = audio.recognize(signal, config.AUTHENTIFIZIERUNG_SAMPLE_RATE)
            name_indexs, name_label_scores = predictor_user.predict(signal)
            print("\n" + "=" * 30)
            print(f"Name = {name_label_scores[0][name_indexs].item()} = {name_label_scores[1][name_indexs].item() * 100}%")
            print("=" * 30)

            (
                anmerkung_satz_labels,
                woerter_anmerkungen,
                absicht_satz_labels,
                absicht_class_scores,
                szenario_satz_labels,
                szenario_class_scores) = predictor_text.predict(text)
            
            print("\n\n" + "=" * 30)
            satz_length = len(woerter_anmerkungen[0])
            for i in range(satz_length):
                print(f"{woerter_anmerkungen[1][i]} = {anmerkung_satz_labels[woerter_anmerkungen[0][i]]} = {woerter_anmerkungen[2][i][woerter_anmerkungen[0][i]] * 100}%")
            print("=" * 30)
            print(f"absicht = {absicht_class_scores[0][absicht_satz_labels]} = {absicht_class_scores[1][absicht_satz_labels] * 100}%")
            print("=" * 30)
            print(f"szenario = {szenario_class_scores[0][szenario_satz_labels]} = {szenario_class_scores[1][szenario_satz_labels] * 100}%")
            print("=" * 30 + "\n\n")
        elif auswahl == '4':
            break
        else:
            print("Ungültige Auswahl, bitte versuche es erneut.")

if __name__ == "__main__":
    main()
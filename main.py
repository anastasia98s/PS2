import webview

from data.data_controller.model import Model
from data.data_controller.view import View
from data.data_controller.presenter import Presenter

from neural_network.predictor import Predictor
from neural_network import train
import config

def main():
    while True:
        print("\nBitte wähle eine Option:")
        print("1. Datenkontrolle")
        print("2. AI Training")
        print("3. Satz eingeben")
        print("4. Beenden")
        
        auswahl = input("Gib die Nummer der Option ein: ")

        if auswahl == '1':
            model = Model()
            view = View()
            presenter = Presenter(model, view)

            webview.create_window('Data Controller', html=view.showPage(1), js_api=presenter)
            webview.start()
        elif auswahl == '2':
            train.run()
        elif auswahl == '3':
            sp_engine = Predictor(config.TRAINED_PATH)
            auswahl = input("Satz: ")
            (
                anmerkung_satz_labels,
                woerter_anmerkungen,
                absicht_satz_labels,
                absicht_class_scores,
                szenario_satz_labels,
                szenario_class_scores) = sp_engine.predict(auswahl)
            
            print("=" * 30)
            satz_length = len(woerter_anmerkungen[0])
            for i in range(satz_length):
                print(f"{woerter_anmerkungen[1][i]} = {anmerkung_satz_labels[woerter_anmerkungen[0][i]]} = {woerter_anmerkungen[2][i][woerter_anmerkungen[0][i]] * 100}%")
            print("=" * 30)
            print(f"absicht = {absicht_class_scores[0][absicht_satz_labels]} = {absicht_class_scores[1][absicht_satz_labels] * 100}%")
            print("=" * 30)
            print(f"szenario = {szenario_class_scores[0][szenario_satz_labels]} = {szenario_class_scores[1][szenario_satz_labels] * 100}%")

        elif auswahl == '4':
            break
        else:
            print("Ungültige Auswahl, bitte versuche es erneut.")

if __name__ == "__main__":
    main()
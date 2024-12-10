from textklassifizierung_controller.presenter import PresenterTextklassifizierung
from nn_textklassifizierung.predictor import Predictor as PredictorText
from nn_textklassifizierung import train as train_textklassifizierung_ki
import config

def main():
    while True:
        print("\n==Textklassifizierung")
        print("Bitte wähle eine Option:")
        print("1. Datenkontrolle")
        print("2. AI Training")
        print("3. Predict")
        print("4. Beenden")
        
        auswahl = input("Gib die Nummer der Option ein: ")

        if auswahl == '1':
            presenter = PresenterTextklassifizierung()
            presenter.open_gui()
        elif auswahl == '2':
            train_textklassifizierung_ki.train()
        elif auswahl == '3':
            predictor_text = PredictorText(config.TEXTKLASSIFIZIERUNG_TRAINED_PATH)
            print("„quit“ zum Beenden\n")
            while True:

                text = input("Satz: ")
                if text == "quit":
                    break

                anmerkung_satz_labels, woerter_anmerkungen, absicht_satz_labels, absicht_class_scores, szenario_satz_labels, szenario_class_scores = predictor_text.predict(text)
                
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
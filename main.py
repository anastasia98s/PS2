from utils.data_controller.textklassifizierung_controller.presenter import PresenterTextklassifizierung
from utils.data_controller.aktivierungswort_controller.presenter import PresenterAktivierungswort
from nn_textklassifizierung.predictor import Predictor as PredictorText
from nn_aktivierungswort import train as train_aktivierungswort_ki
from nn_textklassifizierung import train as train_textklassifizierung_ki
from nn_authentifizierung import train as train_authentifizierung_ki
import config

def main():
    while True:
        print("\nBitte wähle eine Option:")
        print("1. AI Textklassifizierung")
        print("2. AI Authentifizierung")
        print("3. AI Aktivierungswort")
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
        elif auswahl == '2':
            while True:
                print("\n==Authentifizierung")
                print("Bitte wähle eine Option:")
                print("1. AI Training")
                print("2. züruck")
                auswahl = input("Gib die Nummer der Option ein: ")
                
                if auswahl == '1':
                    train_authentifizierung_ki.train()
                if auswahl == '2':
                    break
        elif auswahl == '3':
            presenter = PresenterAktivierungswort()
            while True:
                print("\n==Aktivierungswort")
                print("Bitte wähle eine Option:")
                print("1. Aktivierungswort aufnehmen")
                print("2. Aktivierungswort-AI Training")
                print("3. züruck")
                auswahl = input("Gib die Nummer der Option ein: ")
                
                if auswahl == '1':
                    presenter.aktivierungswort_aufnehmen(config.AKTIVIERUNGSWORT_AUFNAHME_DAUER, config.AUDIO_SAMPLE_RATE)
                if auswahl == '2':
                    train_aktivierungswort_ki.train()
                if auswahl == '3':
                    break
        elif auswahl == '4':
            break
        else:
            print("Ungültige Auswahl, bitte versuche es erneut.")

if __name__ == "__main__":
    main()
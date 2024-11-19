import config
from utils.audio.utils import listen
from neural_network.nn_aktivierungswort.utils import extract_features
from utils.data_controller.aktivierungswort_controller.model_aktivierungswort import ModelAktivierungswort

class PresenterAktivierungswort():
    def __init__(self):
        self.model = ModelAktivierungswort()

    def aktivierungswort_aufnehmen(self, silence_duration, sample_rate):
        while True:
            antwort_signal, antwort_signal_trim = listen(silence_duration, sample_rate)
            
            wort_typ = None
            skip = False
            beenden = False
            print("Speichern Aufnahme als:")
            print("1. Aktivierungswort")
            print("2. kein Aktivierungswort")
            print("3. nicht speichern")
            print("4. nicht speichern und züruck")
            while True:
                antwort = input("Input: ")
                if antwort == '1':
                    print("Antwort: Aktivierungswort")
                    wort_typ = 1
                    break
                elif antwort == '2':
                    print("Antwort: kein Aktivierungswort")
                    wort_typ = 0
                    break
                elif antwort == '3':
                    print("Antwort: nicht speichern")
                    skip = True
                    break
                elif antwort == '4':
                    print("Antwort: nicht speichern und züruck")
                    beenden = True
                    break
            if skip:
                continue
            elif beenden:
                break
            else:
                features = extract_features(antwort_signal, config.AUDIO_SAMPLE_RATE)
                print(features.shape)
                self.model.add_merkmale(features, wort_typ)

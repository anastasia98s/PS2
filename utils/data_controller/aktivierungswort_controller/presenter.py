import config
from utils.audio import Audio
from nn_aktivierungswort.utils import extract_features
from utils.data_controller.aktivierungswort_controller.model_aktivierungswort import ModelAktivierungswort

class PresenterAktivierungswort(Audio):
    def __init__(self):
        self.model = ModelAktivierungswort()

    def aktivierungswort_aufnehmen(self, silence_duration, sample_rate):
        while True:
            antwort_signal, antwort_signal_trim = super().listen(silence_duration, sample_rate, ohne_init=True)
            
            wort_typ = None
            skip = False
            beenden = False
            
            print("1. Wake Word")
            print("2. Not Wake Word")
            print("3. Skip")
            print("4. züruck")
            while True:
                antwort = input("Input: ")
                if antwort == '1':
                    wort_typ = 1
                    break
                elif antwort == '2':
                    wort_typ = 0
                    break
                elif antwort == '3':
                    skip = True
                    break
                elif antwort == '4':
                    beenden = True
                    break
            if skip:
                continue
            elif beenden:
                break
            else:
                features = extract_features(antwort_signal_trim, config.AUDIO_SAMPLE_RATE)
                self.model.add_merkmale(features, wort_typ)

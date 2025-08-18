import config
import librosa
import matplotlib.pyplot as plt
from utils.audio.utils import listen
from aktivierungswort.nn_aktivierungswort.utils import extract_features
from aktivierungswort.aktivierungswort_controller.model_aktivierungswort import ModelAktivierungswort
import utils.api

class PresenterAktivierungswort():
    def __init__(self):
        self.model = ModelAktivierungswort()

    def aktivierungswort_aufnehmen(self, silence_duration, sample_rate):
        while True:
            antwort_signal, antwort_signal_trim = listen(silence_duration, sample_rate)
            titel = None
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
                    titel = "Aktivierungswort"
                    wort_typ = 1
                    break
                elif antwort == '2':
                    titel = "kein Aktivierungswort"
                    wort_typ = 0
                    break
                elif antwort == '3':
                    titel = "nicht speichern"
                    skip = True
                    break
                elif antwort == '4':
                    titel = "nicht speichern und züruck"
                    beenden = True
                    break

            print(f"Antwort: {titel}")
            
            features = extract_features(antwort_signal, utils.api.AUDIO_SAMPLE_RATE)
            if config.AKTIVIERUNGSWORT_AUFNAHME_PLOT:
                plt.figure(figsize=(10, 4))
                librosa.display.specshow(features, sr=22050, hop_length=512, x_axis='time', y_axis='mel')
                plt.colorbar(format='%+2.0f dB')
                plt.title(f'{titel}')
                plt.tight_layout()
                plt.show()
                
            if skip:
                continue
            elif beenden:
                break
            else:
                # features = extract_features(antwort_signal, utils.api.AUDIO_SAMPLE_RATE)
                self.model.add_merkmale(features, wort_typ)

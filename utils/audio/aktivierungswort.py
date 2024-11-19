import config
import threading
from neural_network.nn_aktivierungswort.predictor import Predictor as PredictorAktivierungswort
import utils.audio.utils

class Aktivierungswort:
    def __init__(self):
        self.thread_event = threading.Event()
        self.predictor_aktivierungswort = PredictorAktivierungswort(config.AKTIVIERUNGSWORT_TRAINED_PATH)

    def wake_word_recognize(self, sample_rate):
        if config.AKTIVIERUNGSWORT_IST_AN:
            self.thread_event.clear()
            lock = threading.Lock()

            def recognize_thread(antwort_signal):
                with lock:
                    if antwort_signal is not None and antwort_signal.any() and not self.thread_event.is_set():
                        pred_aktivierung_label = self.predictor_aktivierungswort.predict(antwort_signal)
                        if pred_aktivierung_label == 1:
                            self.thread_event.set()
            threads = []
            while True:
                antwort_signal, _ = utils.audio.utils.listen(config.AKTIVIERUNGSWORT_AUFNAHME_DAUER, sample_rate, max_time=2, status_class_thread=self, save_rec=False)

                if not self.thread_event.is_set():
                    if antwort_signal is not None:
                        thread = threading.Thread(target=recognize_thread, args=(antwort_signal,))
                        thread.start()
                        threads.append(thread)
                else:
                    break
            
            for t in threads:
                t.join()
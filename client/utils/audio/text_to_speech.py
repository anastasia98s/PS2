import config
import os
import utils.api
import base64
import scipy.io.wavfile
import numpy as np

class TextToSpeech:
    def __init__(self):
        pass
            
    def text_to_speech(self, satz, status_class_thread=None):
        if satz:
            if status_class_thread and status_class_thread.thread_event.is_set():
                return None
            
            folder_path = os.path.dirname(config.AUDIO_TMP_PATH)
            os.makedirs(folder_path, exist_ok=True)
            
            wav_binary, error_request = utils.api.text_to_speech_generieren(satz)

            if error_request:
                print(wav_binary)
            elif wav_binary:
                base64_audio = wav_binary
                audio_data = base64.b64decode(base64_audio)
                wav_array = np.frombuffer(audio_data, dtype=np.int16)
                wav_array = wav_array.astype(np.int16)
                scipy.io.wavfile.write(config.AUDIO_TMP_PATH, 22050, wav_array)

                os.system("start " + config.AUDIO_TMP_PATH)
            else:
                print("TTS ERROR!")
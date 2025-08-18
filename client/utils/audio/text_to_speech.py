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
            
            #folder_path = os.path.dirname(config.AUDIO_TMP_PATH)
            os.makedirs(config.AUDIO_DIR, exist_ok=True)
            
            wav_binary, error_request = utils.api.text_to_speech_generieren(satz)

            if error_request:
                print(wav_binary)
            elif wav_binary:
                try:
                    base64_audio = wav_binary
                    audio_data = base64.b64decode(base64_audio)
                    wav_array = np.frombuffer(audio_data, dtype=np.int16)
                    wav_array = wav_array.astype(np.int16)
                    num_index = 1

                    while num_index <= config.MAX_AUDIO_RETRIES:
                        file_path = os.path.join(config.AUDIO_DIR, f"audio_tmp{num_index}.wav")
                        try:
                            scipy.io.wavfile.write(file_path, 22050, wav_array)
                            break
                        except PermissionError:
                            num_index += 1

                    if num_index > config.MAX_AUDIO_RETRIES:
                        print("Sie müssen Ihren Mediaplayer schließen und es noch einmal probieren!")
                    else:
                        os.system("start " + file_path)
                except Exception as e:
                    print(f"Media Player-Fehler!: {e}")
            else:
                print("TTS ERROR!")
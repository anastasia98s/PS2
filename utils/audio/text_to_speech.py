import config
import os

import contextlib
import sys
from TTS.utils.synthesizer import Synthesizer
#from gtts import gTTS

class TextToSpeech:
    def __init__(self):
        
        if not os.path.isfile(config.TTS_TRAINED_PATH) or not os.path.isfile(config.TTS_JSON_PATH):
            raise FileNotFoundError(f"\nTTS Modell / TTS Config nicht gefunden")
        
        self.def_reference_wav = None
        self.def_reference_speaker_idx = None
        self.def_capacitron_style_text = None
        self.def_capacitron_style_wav = None
        self.def_speaker_wav = None
        self.def_language_idx = None
        self.def_speaker_idx = None
        
        def_voice_dir = None
        def_language_ids_file_path = None
        def_speakers_file_path = None
        def_pipe_out = False

        def_config_path = config.TTS_JSON_PATH
        def_model_path = config.TTS_TRAINED_PATH
        self.def_out_path = config.RECORD_TMP_PATH

        self.pipe_out = sys.stdout if def_pipe_out else None

        with contextlib.redirect_stdout(None if def_pipe_out else sys.stdout):
            tts_path = None
            tts_config_path = None
            speakers_file_path = None
            language_ids_file_path = None
            vocoder_path = None
            vocoder_config_path = None
            encoder_path = None
            encoder_config_path = None
            vc_path = None
            vc_config_path = None
            model_dir = None

            if def_model_path is not None:
                tts_path = def_model_path
                tts_config_path = def_config_path
                speakers_file_path = def_speakers_file_path
                language_ids_file_path = def_language_ids_file_path

            self.synthesizer = Synthesizer(
                tts_path,
                tts_config_path,
                speakers_file_path,
                language_ids_file_path,
                vocoder_path,
                vocoder_config_path,
                encoder_path,
                encoder_config_path,
                vc_path,
                vc_config_path,
                model_dir,
                def_voice_dir).to(config.DEVICE)
            
    def text_to_speech(self, satz, status_class_thread=None):
        if satz:
            if status_class_thread and status_class_thread.thread_event.is_set():
                return None
            
            folder_path = os.path.dirname(config.RECORD_TMP_PATH)
            os.makedirs(folder_path, exist_ok=True)
            
            #tts = gTTS(text=satz, lang='de')
            #tts.save(config.RECORD_TMP_PATH)

            wav = self.synthesizer.tts(
                satz,
                speaker_name=self.def_speaker_idx,
                language_name=self.def_language_idx,
                speaker_wav=self.def_speaker_wav,
                reference_wav=self.def_reference_wav,
                style_wav=self.def_capacitron_style_wav,
                style_text=self.def_capacitron_style_text,
                reference_speaker_name=self.def_reference_speaker_idx,
            )

            print(" > Saving output to {}".format(self.def_out_path))
            self.synthesizer.save_wav(wav, self.def_out_path, pipe_out=self.pipe_out)

            os.system("start " + config.RECORD_TMP_PATH)
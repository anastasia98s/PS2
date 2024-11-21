import wave
import numpy as np
import os
import config
import librosa
import pyaudio
import time

def listen(silence_duration, sample_rate, max_time=config.MAX_RECORDING_TIME, status_class_thread=None, save_rec=True):
    audio = pyaudio.PyAudio()
    chunk = 1024
    stream = audio.open( format=pyaudio.paInt16,
                                channels=1,
                                rate=sample_rate,
                                input=True,
                                frames_per_buffer=chunk)

    recording = []
    silent_chunks = 0
    silence_limit = int(silence_duration * sample_rate)
    last_chunks = None
    is_recording = True

    recording_runden = 1
    recording_animation_index = 0
    recording_start_time = None
    
    while is_recording:

        if status_class_thread:
            if status_class_thread.thread_event.is_set():
                return None, None
        try:
            audio_chunk = stream.read(chunk)
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
            amplitude = np.abs(audio_data).mean()

            if recording_runden % 5 == 0 or recording_runden == 1:
                if recording_animation_index == 5:
                    recording_animation_index = 0
                print("\r", "Frame: " + str(len(recording)) + " |Amplitude: " + str(round(amplitude)) + "/"+ str(config.AUDIO_THRESHOLD) + " |Bitte sprechen Sie" + "." * recording_animation_index, end="", flush=True)
                recording_animation_index += 1
            recording_runden += 1

            if amplitude > config.AUDIO_THRESHOLD:
                if not recording_start_time:
                    recording_start_time = time.time()
                if not recording and last_chunks is not None:
                    recording.append(last_chunks)
                recording.append(audio_chunk)
                silent_chunks = 0
            else:
                if recording_start_time is not None:
                    silent_chunks += len(audio_chunk)
                    if silent_chunks > silence_limit and recording:
                        recording.append(audio_chunk)
                        print("\nAufnahme beendet")
                        is_recording = False
                    elif recording:
                        recording.append(audio_chunk)

            last_chunks = audio_chunk
            if recording_start_time is not None and (time.time() - recording_start_time) > max_time:
                print("\nTime Out!")
                is_recording = False
        except KeyboardInterrupt:
            is_recording = False

    stream.stop_stream()
    stream.close()
    audio.terminate()

    recording_concat = np.concatenate([np.frombuffer(chunk, dtype=np.int16) for chunk in recording])

    # Audioqualität testen
    if save_rec:
        folder_path = os.path.dirname(config.RECORD_TMP_PATH)
        os.makedirs(folder_path, exist_ok=True)
        with wave.open(config.RECORD_TMP_PATH, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(recording_concat.tobytes())

    recording_flat = recording_concat.flatten().astype(np.float32)
    recording_trim, _ = librosa.effects.trim(recording_flat, top_db=config.AUDIO_DB)
    return recording_flat, recording_trim
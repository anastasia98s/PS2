import config
from neural_network.nn_authentifizierung.utils import extract_features
from utils.data_controller.user_controller.model_user import ModelUser

class PresenterUser:
    def __init__(self):
        self.model = ModelUser()

    def save_features(self, signal, benutzer_id):
        target_length = config.AUDIO_SIGNAL_LENGTH_SAVE
        signal_length = len(signal)
        num_parts = (signal_length - target_length) // target_length
        
        for i in range(num_parts):
            signal_part = signal[i * target_length : (i + 1) * target_length]
            features = extract_features(signal_part, config.AUDIO_SAMPLE_RATE)
            self.model.add_merkmale(benutzer_id, features)
        
        remainder_length = signal_length % target_length
        if remainder_length > 0:
            signal_part = signal[num_parts * target_length:]
            features = extract_features(signal_part, config.AUDIO_SAMPLE_RATE)
            self.model.add_merkmale(benutzer_id, features)
    
    def show_benutzer_name(self, benutzer_id):
        return self.model.show_benutzer_name(benutzer_id)
    
    def add_benutzer(self, name):
        return self.model.add_benutzer(name)
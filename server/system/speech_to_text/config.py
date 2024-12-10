import torch

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
NO_SPEECH_MAX_NOTEN = 0.85
SPEECH_RECOGNITION_MODELL = "large"
WHISPER_SPRACHE = 'de'
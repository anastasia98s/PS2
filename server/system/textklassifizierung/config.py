import transformers
import torch

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
TEXTKLASSIFIZIERUNG_DATASET_PATH  = 'data/textklassifizierung.db'
TEXTKLASSIFIZIERUNG_TRAINED_PATH = 'data/textklassifizierung.pth'
TEXTKLASSIFIZIERUNG_META_PATH = 'data/textklassifizierung_meta.bin'

TEXTKLASSIFIZIERUNG_BASE_MODEL = 'dbmdz/bert-base-german-uncased'
TEXTKLASSIFIZIERUNG_TOKENIZER = transformers.BertTokenizer.from_pretrained(TEXTKLASSIFIZIERUNG_BASE_MODEL, do_lower_case = True)

TEXTKLASSIFIZIERUNG_MAX_LEN = 70
TEXTKLASSIFIZIERUNG_TRAIN_BATCH_SIZE = 50
TEXTKLASSIFIZIERUNG_VALIDATION_BATCH_SIZE = 50
TEXTKLASSIFIZIERUNG_EPOCHS = 100

TEXTKLASSIFIZIERUNG_SAVE_MODEL = True
TEXTKLASSIFIZIERUNG_RETRAIN_MODEL = False
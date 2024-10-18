import transformers
import torch

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

DATASET_PATH  = 'data/dataset/data.db'
TRAINED_PATH = 'data/result/trained_data.pth'
META_PATH = 'data/meta_data.bin'

BASE_MODEL = 'dbmdz/bert-base-german-uncased'
TOKENIZER = transformers.BertTokenizer.from_pretrained(
    BASE_MODEL,
    do_lower_case = True
)

MAX_LEN = 50
TRAIN_BATCH_SIZE = 50
TEST_BATCH_SIZE = 50
EPOCHS = 50

SAVE_MODEL = True
RETRAIN_MODEL = False
import pandas as pd
import spacy
import random
from spacy.training import Example
from tqdm import tqdm
import sys

DEFAULT_TRAIN_DATA = "default_train_data.csv"
DEFAULT_MODEL = "nlp_model_trf"

def read_train_data(custom: bool = False):
    train_data_csv = DEFAULT_TRAIN_DATA if not custom else "wiki_train_data.csv"
    df = pd.read_csv(train_data_csv)

    train_data = []
    
    for _, row in df.iterrows():
        text = row["text"]
        entities = []
        
        for i in range(20):  # Loop through max 10 entities
            start_col = f"start{i}"
            text_col = f"text{i}"
            label_col = f"label{i}"
            try:
                if pd.notna(row[start_col]) and pd.notna(row[text_col]) and pd.notna(row[label_col]):
                    start = int(row[start_col])
                    end = start + len(row[text_col])  # Compute end position
                    label = row[label_col]
                    entities.append((start, end, label))
            except:
                break
        
        if entities:
            train_data.append((text, {"entities": entities}))

    print(f"Loaded {len(train_data)} samples for training")
    return train_data

def train(custom: bool = False):
    nlp = spacy.load("en_core_web_trf")

    ner = nlp.get_pipe("ner")

    train_data = read_train_data()

    for _, annotations in train_data:
        for ent in annotations["entities"]:
            ner.add_label(ent[2])
    print("Labels added to NER pipeline")

    optimizer = nlp.create_optimizer()

    for epoch in range(20):
        random.shuffle(train_data)
        losses = {}

        #KB tqdm is used for progress bar
        for text, annotations in tqdm(train_data, desc=f"Epoch {epoch+1}"):
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.2, losses=losses, sgd=optimizer)
        print(f"Epoch {epoch + 1} loss: {losses}")

    model_jo = DEFAULT_MODEL if not custom else "wiki_model_trf"
    nlp.to_disk(model_jo) 
    print("Training completed and model saved")


if sys.argv[1] == "wiki":
    train(custom=True)
else:
    train()

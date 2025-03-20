import pandas as pd
import spacy
import random
from spacy.training import Example
from tqdm import tqdm

def read_train_data():
    df = pd.read_csv("train_data.csv")

    train_data = []
    
    for _, row in df.iterrows():
        text = row["text"]
        entities = []
        
        for i in range(10):  # Loop through max 10 entities
            start_col = f"start{i}"
            text_col = f"text{i}"
            label_col = f"label{i}"
            
            if pd.notna(row[start_col]) and pd.notna(row[text_col]) and pd.notna(row[label_col]):
                start = int(row[start_col])
                end = start + len(row[text_col])  # Compute end position
                label = row[label_col]
                entities.append((start, end, label))
        
        if entities:
            train_data.append((text, {"entities": entities}))

    print(f"Loaded {len(train_data)} samples for training")
    return train_data

def train():
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

        for text, annotations in tqdm(train_data, desc=f"Epoch {epoch+1}"):
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.2, losses=losses)
        print(f"Epoch {epoch + 1} loss: {losses}")

    nlp.to_disk("nlp_model_trf")
    print("Training completed and model saved")

# Run training
train()

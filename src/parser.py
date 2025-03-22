import wikipediaapi
import spacy
import pandas as pd
from dotenv import load_dotenv
import os
import sys
import re

load_dotenv()

nlp = spacy.load("nlp_model_trf")
USER_AGENT: str = os.getenv("WIKI_USER_AGENT","Default")
WIKI_TRAIN_DATA = "wiki_train_data.csv"

def get_wikipedia_article(title):
     wiki = wikipediaapi.Wikipedia(user_agent=USER_AGENT ,language="en")
     page = wiki.page(title)
     return page.text if page.exists() else None

def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if len(s) > 5]

def extract_entities(lines):
    data = []
    
    for line in lines:
        doc = nlp(line)
        row = [line]

        for ent in doc.ents:
            row.extend([ent.start_char, ent.text, ent.label_])
        data.append(row)
    
    return data

def save(entity_data):
    max_entities = max(len(row) for row in entity_data) - 1
    headers = ["text"]
    for i in range(max_entities // 3):
        headers.extend([f"start{i}", f"text{i}", f"label{i}"])


    df = pd.DataFrame(entity_data, columns=headers)
    df.to_csv(WIKI_TRAIN_DATA, index=False)

    print("File saved")

article_name = sys.argv[1]
print(f"wikipedia_article: {article_name}")
article = get_wikipedia_article(article_name)
if article:
    data = split_into_sentences(article)
    entity_data = extract_entities(data)
    save(entity_data)
else:
    print("No such article was found")
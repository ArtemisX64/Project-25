from flask import Flask, request, render_template, jsonify
import spacy
import wikipediaapi
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import base64
import sys
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

app = Flask(__name__)

model:str = "nlp_model_trf"
try:
    model:str = "wiki_model_trf" if sys.argv[1] == "wiki" else "nlp_model_trf"
    print("Using wiki model")
except:
    print("Using default model")

nlp = spacy.load(model)
USER_AGENT: str = os.getenv("WIKI_USER_AGENT","Default")

def get_article(title: str):
    wiki = wikipediaapi.Wikipedia(user_agent=USER_AGENT, language="en")
    page = wiki.page(title)
    return page.text if page.exists() else None

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def extract_entities(text):
    doc = nlp(text)
    entities = []
    entity_count = {}
    entity_colors = {}

    for ent in doc.ents:
        if ent.label_ not in entity_colors:
            color = random_color()
            while color in entity_colors.values():
                color = random_color()

            entity_colors[ent.label_] = color
        wiki_link = None
        if ent.label_ in ["PERSON", "GPE", "ORG"]:
            wiki_link = f"https://en.wikipedia.org/wiki/{ent.text.replace(' ', '_')}"
        entities.append({"text": ent.text, "start": ent.start_char, "label": ent.label_, "wiki_link": wiki_link})
        entity_count[ent.label_] = entity_count.get(ent.label_,0) + 1
    return entities, entity_count, entity_colors

def gen_pie(entity_count:dict, entity_colors):
    labels = list(entity_count.keys())
    sizes = list(entity_count.values())
    colors = [entity_colors[label] for label in labels]

    plt.figure(figsize=(5,5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    plt.axis('equal')

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded_img = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return f"data:image/png;base64,{encoded_img}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    text = data.get("text", "") 

    if not text:
        return jsonify({"error": "Article not found"})

    entities, entity_count, entity_colors = extract_entities(text)
        
    pie_chart = gen_pie(entity_count, entity_colors)

    return jsonify({"text": text, "entities": entities, "pie_chart": pie_chart, "entity_colors": entity_colors})

app.run()
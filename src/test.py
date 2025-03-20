import spacy
nlp = spacy.load("nlp_model_trf")  # Load best trained model
doc = nlp("Pluto is discovered by  Jobins")
for ent in doc.ents:
    print(ent.text, ent.label_)
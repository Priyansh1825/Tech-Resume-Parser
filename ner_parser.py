import spacy

# Load the large English NLP model
nlp = spacy.load("en_core_web_lg")

def extract_entities(text):
    """
    Processes text through SpaCy to identify standard entities.
    """
    doc = nlp(text)
    entities = {}
    
    for ent in doc.ents:
        # We store entities in a dictionary, grouping multiple values per label
        if ent.label_ not in entities:
            entities[ent.label_] = [ent.text]
        else:
            if ent.text not in entities[ent.label_]:
                entities[ent.label_].append(ent.text)
                
    return entities

# Example of labels we expect: 'PERSON', 'ORG' (Companies/Uni), 'GPE' (Locations)
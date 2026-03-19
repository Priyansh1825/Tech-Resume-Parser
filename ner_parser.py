import spacy

# Load the large English model
# This model uses word embeddings to understand context [cite: 76]
nlp = spacy.load("en_core_web_lg")

def extract_basic_entities(cleaned_text):
    """
    Uses SpaCy's pre-trained NER to find names, organizations, and locations.
    """
    doc = nlp(cleaned_text)
    extracted_data = {}

    for ent in doc.ents:
        # We only care about specific labels for a tech resume
        if ent.label_ in ["PERSON", "ORG", "GPE", "DATE"]:
            if ent.label_ not in extracted_data:
                extracted_data[ent.label_] = []
            
            # Avoid duplicate entries
            if ent.text not in extracted_data[ent.label_]:
                extracted_data[ent.label_].append(ent.text)
    
    return extracted_data

# Example Test
if __name__ == "__main__":
    sample_text = "Priyansh Umeshbhai worked at Jain University in Bengaluru during 2025."
    entities = extract_basic_entities(sample_text)
    print(entities)
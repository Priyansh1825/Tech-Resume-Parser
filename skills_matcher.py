import spacy
from spacy.pipeline import EntityRuler

def add_custom_ner_rules(nlp):
    """
    Adds custom rules to identify Skills and Education.
    """
    # Initialize the EntityRuler
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    
    # Define patterns for Skills (Add more based on your Kaggle dataset)
    patterns = [
        {"label": "SKILL", "pattern": "Python"},
        {"label": "SKILL", "pattern": "Machine Learning"},
        {"label": "SKILL", "pattern": "NLP"},
        {"label": "SKILL", "pattern": "Deep Learning"},
        {"label": "SKILL", "pattern": "SpaCy"},
        {"label": "SKILL", "pattern": "SQL"},
        # Patterns for Education/Degrees
        {"label": "DEGREE", "pattern": [{"LOWER": "master"}, {"LOWER": "of"}, {"LOWER": "technology"}]},
        {"label": "DEGREE", "pattern": [{"LOWER": "bachelor"}, {"LOWER": "of"}, {"LOWER": "engineering"}]},
        {"label": "DEGREE", "pattern": "M.Tech"},
        {"label": "DEGREE", "pattern": "B.E"}
    ]
    
    ruler.add_patterns(patterns)
    return nlp

# Example usage:
# nlp = spacy.load("en_core_web_lg")
# nlp = add_custom_ner_rules(nlp)
# doc = nlp("Priyansh has a Master of Technology and knows Python.")
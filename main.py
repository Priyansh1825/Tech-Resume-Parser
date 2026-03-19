import json
import os
from extractor import get_resume_text
from preprocess import clean_text
from ner_parser import nlp, extract_basic_entities
from skills_matcher import add_custom_ner_rules

# Initialize the NLP pipeline with custom rules
nlp_custom = add_custom_ner_rules(nlp)

def parse_resume(file_path):
    # 1. Extraction [cite: 65]
    raw_text = get_resume_text(file_path)
    
    # 2. Preprocessing [cite: 64]
    cleaned = clean_text(raw_text)
    
    # 3. NER Processing [cite: 26, 79]
    doc = nlp_custom(cleaned)
    
    results = {
        "candidate_info": {},
        "technical_skills": [],
        "education": []
    }
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            results["candidate_info"]["name"] = ent.text
        elif ent.label_ == "GPE":
            results["candidate_info"]["location"] = ent.text
        elif ent.label_ == "SKILL":
            if ent.text not in results["technical_skills"]:
                results["technical_skills"].append(ent.text)
        elif ent.label_ == "DEGREE":
            if ent.text not in results["education"]:
                results["education"].append(ent.text)
                
    return results

def save_to_json(data, output_filename="parsed_resume.json"):
    with open(output_filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Success: Results saved to {output_filename}")

# Test execution
if __name__ == "__main__":
    # Ensure you have a test file in your data/raw folder
    sample_path = 'data/raw/test_resume.pdf'
    if os.path.exists(sample_path):
        data = parse_resume(sample_path)
        save_to_json(data)
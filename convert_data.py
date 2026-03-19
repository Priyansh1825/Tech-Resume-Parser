import spacy
from spacy.tokens import DocBin
import json
import os

def convert_dataturks_to_spacy(json_filepath, output_path):
    nlp = spacy.blank("en") # Start with a blank English model
    db = DocBin()
    
    with open(json_filepath, 'r', encoding='utf-8') as f:
        # The Kaggle file contains one JSON object per line
        for line in f:
            data = json.loads(line)
            text = data.get('content', '')
            annotations = data.get('annotation', [])
            
            doc = nlp.make_doc(text)
            ents = []
            
            if annotations is not None:
                for annot in annotations:
                    # SAFETY CHECK: Skip if the label is missing or is an empty list
                    if not annot.get('label') or (isinstance(annot['label'], list) and len(annot['label']) == 0):
                        continue
                        
                    # Extract the label, start, and end points
                    label = annot['label'][0] if isinstance(annot['label'], list) else annot['label']
                    start = annot['points'][0]['start']
                    end = annot['points'][0]['end'] + 1 # +1 because Python slicing is exclusive
                    
                    # Create a span for the entity
                    span = doc.char_span(start, end, label=label, alignment_mode="contract")
                    if span is not None:
                        ents.append(span)
            
            # Filter out overlapping entities to prevent training errors
            filtered_ents = spacy.util.filter_spans(ents)
            doc.ents = filtered_ents
            db.add(doc)
            
    # Save the binary file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    db.to_disk(output_path)
    print(f"Success! Data converted and saved to {output_path}")

if __name__ == "__main__":
    # The exact filename from the Kaggle download
    input_file = "data/raw/Entity Recognition in Resumes.json"
    output_file = "data/train.spacy"
    
    if os.path.exists(input_file):
        convert_dataturks_to_spacy(input_file, output_file)
    else:
        print(f"Error: Could not find {input_file}. Please check the folder.")
        
import spacy
from spacy.tokens import DocBin
import json
import os

def convert_dataturks_to_spacy(json_filepath, output_path):
    nlp = spacy.blank("en") # Start with a blank English model
    db = DocBin()
    
    with open(json_filepath, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            text = data.get('content', '')
            annotations = data.get('annotation', [])
            
            doc = nlp.make_doc(text)
            ents = []
            
            if annotations is not None:
                for annot in annotations:
                    # Skip empty labels
                    if not annot.get('label') or (isinstance(annot['label'], list) and len(annot['label']) == 0):
                        continue
                        
                    label = annot['label'][0] if isinstance(annot['label'], list) else annot['label']
                    start = annot['points'][0]['start']
                    end = annot['points'][0]['end'] + 1
                    
                    # Contract the span to snap to valid token boundaries
                    span = doc.char_span(start, end, label=label, alignment_mode="contract")
                    
                    # THE FIX: Strict Validation for E024
                    if span is not None:
                        span_text = span.text
                        # 1. Reject if it contains a newline character
                        # 2. Reject if it is just empty spaces
                        # 3. Reject if it has leading/trailing whitespaces that slipped through
                        if '\n' not in span_text and span_text.strip() != "":
                            if span_text == span_text.strip():
                                ents.append(span)
            
            # Filter out overlapping entities
            filtered_ents = spacy.util.filter_spans(ents)
            doc.ents = filtered_ents
            db.add(doc)
            
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    db.to_disk(output_path)
    print(f"Success! Cleaned data saved to {output_path}")

if __name__ == "__main__":
    # Ensure this matches the exact filename you downloaded
    input_file = "data/raw/Entity Recognition in Resumes.json"
    output_file = "data/train.spacy"
    
    if os.path.exists(input_file):
        convert_dataturks_to_spacy(input_file, output_file)
    else:
        print(f"Error: Could not find {input_file}")
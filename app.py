import streamlit as st
import spacy
import pdfminer.high_level
import docx2txt
import tempfile
import os

st.set_page_config(page_title="Tech Resume Parser", page_icon="📄")
st.title("📄 Tech Resume Parser (NER)")
st.write("Upload a candidate's resume (PDF or DOCX) to instantly extract key entities.")

@st.cache_resource
def load_ner_model():
    model_path = "./models/model-best" 
    if os.path.exists(model_path):
        return spacy.load(model_path)
    else:
        st.error(f"Model not found at {model_path}. Please train the model first.")
        return None

nlp = load_ner_model()

uploaded_file = st.file_uploader("Upload Resume Document", type=["pdf", "docx"])

if uploaded_file is not None and nlp is not None:
    st.info("Processing document...")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    try:
        raw_text = ""
        if uploaded_file.name.lower().endswith('.pdf'):
            raw_text = pdfminer.high_level.extract_text(tmp_path)
        elif uploaded_file.name.lower().endswith('.docx'):
            raw_text = docx2txt.process(tmp_path)
            
        os.remove(tmp_path)

        if raw_text.strip():
            st.success("Analysis Complete!")
            doc = nlp(raw_text)
            
            # --- NEW LOGIC: Separate Technical Skills from other entities ---
            technical_skills = set()
            other_entities = {}
            
            for ent in doc.ents:
                label = ent.label_.upper() # Normalize to uppercase
                text = ent.text.replace('\n', ' ').strip()
                
                # Check if the label contains the word 'SKILL'
                if 'SKILL' in label:
                    technical_skills.add(text)
                else:
                    if label not in other_entities:
                        other_entities[label] = set()
                    other_entities[label].add(text)
                    
            st.divider()
            
            # 1. Display Technical Skills Prominently
            st.subheader("💻 Technical Skills")
            if technical_skills:
                # Display as a comma-separated list or badges
                st.markdown(f"**{', '.join(technical_skills)}**")
            else:
                st.warning("No technical skills were explicitly identified by the model.")
                
            st.divider()
            
            # 2. Display the rest of the extracted information
            st.subheader("📋 Other Extracted Information")
            if other_entities:
                for label, items in other_entities.items():
                    with st.expander(f"{label} ({len(items)})"):
                        for item in items:
                            st.markdown(f"- {item}")
            else:
                st.info("No other entities found.")
                
        else:
            st.error("The document appears to be empty.")
            
    except Exception as e:
        st.error(f"An error occurred during processing: {e}")
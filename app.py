import streamlit as st
import spacy
from spacy import displacy
import pdfminer.high_level
import docx2txt
import tempfile
import os
import json

# 1. Page Configuration
st.set_page_config(page_title="Tech Resume Parser", page_icon="🚀", layout="wide")

# 2. Advanced Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #1E3A8A; font-weight: 800; margin-bottom: 0px; }
    .sub-header { font-size: 1.2rem; color: #6B7280; margin-bottom: 30px; }
    .entity-card { background-color: #F3F4F6; padding: 15px; border-radius: 10px; border-left: 5px solid #3B82F6; margin-bottom: 10px; }
    .entity-label { font-weight: bold; color: #1F2937; font-size: 1.1rem; }
    .entity-value { color: #4B5563; font-family: monospace; background-color: #E5E7EB; padding: 2px 6px; border-radius: 4px; margin: 2px; display: inline-block; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_ner_model():
    model_path = "./models/model-best" 
    if os.path.exists(model_path):
        return spacy.load(model_path)
    return None

nlp = load_ner_model()

# 3. Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/942/942748.png", width=100) 
    st.markdown("## Upload Resume")
    uploaded_file = st.file_uploader("Drop PDF or DOCX here", type=["pdf", "docx"])
    
    st.markdown("---")
    st.markdown("### 🎓 Project Details")
    st.markdown("**Tech Resume Parser (NER)**")
    st.markdown("By: Priyansh & Raj")
    st.markdown("*Dept. of Artificial Intelligence*")

st.markdown('<p class="main-header">🚀 Intelligent Tech Resume Parser</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-driven entity extraction with human-in-the-loop validation.</p>', unsafe_allow_html=True)

if uploaded_file is not None and nlp is not None:
    with st.spinner("🧠 AI is analyzing the document..."):
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
                doc = nlp(raw_text)
                
                technical_skills = set()
                other_entities = {}
                
                for ent in doc.ents:
                    label = ent.label_.upper()
                    text = ent.text.replace('\n', ' ').strip()
                    if text:
                        if 'SKILL' in label:
                            technical_skills.add(text)
                        else:
                            if label not in other_entities:
                                other_entities[label] = set()
                            other_entities[label].add(text)
                
                st.toast(f"Successfully processed {uploaded_file.name}!", icon="✅")
                
                # --- INTERACTIVE TABS ---
                tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔍 Interactive Visualizer", "✏️ Review & Export"])
                
                # TAB 1: Visual Dashboard (Same as before but cleaner)
                with tab1:
                    col1, col2, col3 = st.columns(3)
                    col1.metric(label="Technical Skills Found", value=len(technical_skills))
                    col2.metric(label="Other Entities Found", value=sum(len(v) for v in other_entities.values()))
                    col3.metric(label="File Format", value=uploaded_file.name.split('.')[-1].upper())
                    
                    st.markdown("---")
                    st.markdown("### 📋 Candidate Details")
                    if other_entities:
                        for label, items in other_entities.items():
                            items_html = "".join([f'<span class="entity-value">{item}</span>' for item in items])
                            st.markdown(f"""
                            <div class="entity-card">
                                <span class="entity-label">{label}</span><br>
                                {items_html}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No additional entities found.")

                # TAB 2: INTERACTIVE TEXT VISUALIZER
                with tab2:
                    st.markdown("### 🔍 Highlighted Entity Visualizer")
                    st.write("Explore how the AI mapped the entities directly within the document's text.")
                    
                    # Generate HTML for the highlighted text
                    html = displacy.render(doc, style="ent", page=False)
                    
                    # Display it in a scrollable, styled container
                    st.markdown(f"""
                        <div style="padding: 20px; background-color: #ffffff; border-radius: 10px; border: 1px solid #e5e7eb; height: 500px; overflow-y: scroll;">
                            {html}
                        </div>
                    """, unsafe_allow_html=True)

                # TAB 3: HUMAN-IN-THE-LOOP EDITING & EXPORT
                with tab3:
                    st.markdown("### ✏️ Validate & Export Data")
                    st.write("Review the AI's findings. You can manually add missing skills or remove incorrect ones before exporting to your ATS.")
                    
                    # Interactive Multi-Select Box
                    # This pre-loads the AI's findings, but lets the user edit them!
                    edited_skills = st.multiselect(
                        "Review Technical Skills (Type to add new ones):",
                        options=list(technical_skills),
                        default=list(technical_skills)
                    )
                    
                    st.markdown("---")
                    
                    # Prepare data based on the EDITED skills, not just the raw AI output
                    export_data = {
                        "filename": uploaded_file.name,
                        "validated_skills": edited_skills,
                        "other_entities": {k: list(v) for k, v in other_entities.items()}
                    }
                    
                    json_string = json.dumps(export_data, indent=4)
                    
                    colA, colB = st.columns([1, 1])
                    with colA:
                        st.download_button(
                            label="📥 Download Validated JSON",
                            file_name=f"{uploaded_file.name}_validated.json",
                            mime="application/json",
                            data=json_string,
                            type="primary",
                            use_container_width=True
                        )
                    with colB:
                        with st.expander("Preview JSON Output"):
                            st.json(export_data)
                        
            else:
                st.error("The document appears to be empty.")
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")
else:
    st.info("👈 Please upload a PDF or DOCX resume from the sidebar to begin.")
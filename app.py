import streamlit as st
import sqlite3
import spacy
import fitz  
import docx2txt
import pytesseract
from PIL import Image
import tempfile
import os
import json
import re
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ==========================================
# 1. NEON DARK MODE & PREMIUM CSS
# ==========================================
st.set_page_config(page_title="AI Recruiter Pro", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; background-color: #0B0F19; color: #E2E8F0; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    .main-title { font-size: 2.8rem; font-weight: 800; background: linear-gradient(to right, #A855F7, #3B82F6, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); }
    
    .metric-grid { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 30px; }
    .metric-card { flex: 1; min-width: 200px; background: #111827; border-radius: 12px; padding: 20px; border: 1px solid #1F2937; border-top: 4px solid #8B5CF6; box-shadow: 0 4px 20px rgba(0,0,0,0.4); transition: transform 0.3s ease; }
    .metric-card:hover { transform: translateY(-5px); border-top: 4px solid #06B6D4; }
    .metric-title { font-size: 1rem; color: #94A3B8; font-weight: 500; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;}
    .metric-value { font-size: 2.2rem; font-weight: 800; color: #F8FAFC; margin: 0;}
    
    .dark-card { background: linear-gradient(180deg, rgba(30,41,59,1) 0%, rgba(15,23,42,1) 100%); border: 1px solid #334155; border-radius: 16px; padding: 25px; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .profile-header { display: flex; align-items: center; gap: 20px; margin-bottom: 20px; }
    .avatar-box { background: linear-gradient(135deg, #8B5CF6, #3B82F6); color: white; font-size: 2.2rem; border-radius: 16px; height: 70px; width: 70px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4); }
    .cand-name { font-size: 1.8rem; font-weight: 700; color: #F8FAFC; margin: 0 0 5px 0; }
    .cand-contact { color: #06B6D4; font-size: 1rem; font-weight: 500; margin: 0; }
    
    .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05); }
    .info-item { display: flex; align-items: flex-start; gap: 10px; }
    .info-icon { font-size: 1.2rem; margin-top: 2px; }
    .info-text-block { display: flex; flex-direction: column; }
    .info-label { color: #64748B; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;}
    .info-data { color: #E2E8F0; font-size: 1rem; font-weight: 500; }
    
    .pill-matched { background: rgba(16, 185, 129, 0.1); color: #34D399; border: 1px solid #10B981; padding: 6px 16px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; display: inline-block; margin: 4px; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2); }
    .pill-missing { background: rgba(239, 68, 68, 0.1); color: #F87171; border: 1px solid #EF4444; padding: 6px 16px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; display: inline-block; margin: 4px; text-decoration: line-through; }
    .pill-neutral { background: rgba(59, 130, 246, 0.1); color: #93C5FD; border: 1px solid #3B82F6; padding: 6px 16px; border-radius: 8px; font-size: 0.85rem; font-weight: 500; display: inline-block; margin: 4px; }
    
    .score-high { background: linear-gradient(135deg, #059669, #10B981); color: white; padding: 10px 20px; border-radius: 10px; font-weight: 800; text-align: center; font-size: 1.3rem; box-shadow: 0 4px 15px rgba(16,185,129,0.4); }
    .score-med { background: linear-gradient(135deg, #D97706, #F59E0B); color: white; padding: 10px 20px; border-radius: 10px; font-weight: 800; text-align: center; font-size: 1.3rem; box-shadow: 0 4px 15px rgba(245,158,11,0.4); }
    .score-low { background: linear-gradient(135deg, #DC2626, #EF4444); color: white; padding: 10px 20px; border-radius: 10px; font-weight: 800; text-align: center; font-size: 1.3rem; box-shadow: 0 4px 15px rgba(239,68,68,0.4); }
</style>
""", unsafe_allow_html=True)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ==========================================
# 2. DATABASE INIT
# ==========================================
def init_db():
    conn = sqlite3.connect('ats_system.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, role_title TEXT, required_skills TEXT, min_experience INTEGER, required_education TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (id INTEGER PRIMARY KEY AUTOINCREMENT, job_id INTEGER, job_role TEXT, name TEXT, email TEXT, phone TEXT, education TEXT, experience TEXT, skills TEXT, match_score REAL, matched_skills TEXT, missing_skills TEXT)''')
    conn.commit()
    conn.close()

init_db()
def get_db_connection():
    conn = sqlite3.connect('ats_system.db')
    conn.row_factory = sqlite3.Row
    return conn

def delete_candidate(cand_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM candidates WHERE id = ?', (cand_id,))
    conn.commit()
    conn.close()

# ==========================================
# 3. AI & SEMANTIC EMBEDDING LOGIC
# ==========================================
@st.cache_resource
def load_models():
    # Load NER Model
    model_path = "./models/model-best" 
    ner = spacy.load(model_path) if os.path.exists(model_path) else (spacy.load("en_core_web_sm") if os.path.exists("en_core_web_sm") else spacy.blank("en"))
    
    # Load ML Classifier
    clf = joblib.load("role_classifier_model.pkl") if os.path.exists("role_classifier_model.pkl") else None
    
    # Load HuggingFace Embedding Model (This provides the Semantic Search!)
    embedder = SentenceTransformer('all-MiniLM-L6-v2') 
    
    return ner, clf, embedder

nlp, role_classifier, embedding_model = load_models()

def extract_text_from_file(uploaded_file):
    ext = uploaded_file.name.split('.')[-1].lower()
    text = ""
    try:
        if ext == 'pdf':
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for page in doc:
                extracted = page.get_text()
                if extracted and extracted.strip(): text += extracted + " \n"
                else:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text += pytesseract.image_to_string(img) + " \n"
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            if ext == 'docx': text = docx2txt.process(tmp_path)
            elif ext in ['png', 'jpg', 'jpeg']: text = pytesseract.image_to_string(Image.open(tmp_path))
            os.remove(tmp_path)
    except Exception as e: st.error(f"Error reading {uploaded_file.name}: {e}")
    return text

def parse_resume(text, filename):
    doc = nlp(text)
    email = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    phone = re.findall(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4,5}\b', text)
    skills = set()
    education = "Not explicitly found"
    experience = "Not explicitly found"
    
    fallback_name = re.sub(r'[^a-zA-Z\s]', '', filename.split('.')[0]).strip()
    name = fallback_name if fallback_name else "Unknown Candidate"
    
    for ent in doc.ents:
        label = ent.label_.upper()
        clean_text = ent.text.replace('\n', ' ').strip()
        if 'SKILL' in label or label == 'ORG': skills.add(clean_text)
        elif label == 'PERSON' and name == fallback_name: name = clean_text 

    # We keep a small fallback list just in case NER misses basic things
    text_lower = text.lower()
    common_tech_skills = ['python', 'java', 'c++', 'javascript', 'react', 'node.js', 'sql', 'aws', 'docker', 'machine learning', 'html', 'css', 'git']
    for skill in common_tech_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower): skills.add(skill.title()) 

    edu_match = re.search(r'\b(bachelor|master|phd|b\.?tech|m\.?tech|b\.?e\.?|b\.?sc|m\.?sc|b\.?c\.?a|m\.?c\.?a|mba)\b.*\n?', text_lower)
    if edu_match: education = edu_match.group(0).title().strip()
    elif re.search(r'\b(university|college|institute|degree)\b', text_lower): education = "University Degree Detected"

    exp_match = re.search(r'(\d+)\+?\s*(years?|yrs?|months?)\s*(of)?\s*experience', text_lower)
    if exp_match: experience = f"{exp_match.group(1)} {exp_match.group(2).capitalize()} Professional Experience"
            
    return {"name": name.title(), "email": email[0] if email else "N/A", "phone": phone[0] if phone else "N/A", "skills": list(skills), "education": education, "experience": experience}

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("## 🚀 AI Recruiter Pro")
    st.markdown("---")
    page = st.radio("System Menu", ["📊 Intelligence Dashboard", "⚙️ Database & Upload", "👥 Candidate Pipeline"])
    st.markdown("---")
    st.caption("M.Tech Project | Priyansh & Raj")

# ==========================================
# PAGE 1: DASHBOARD
# ==========================================
if page == "📊 Intelligence Dashboard":
    st.markdown('<div class="main-title">Intelligence Dashboard</div>', unsafe_allow_html=True)
    
    conn = get_db_connection()
    jobs_count = conn.execute('SELECT COUNT(*) FROM jobs').fetchone()[0]
    cands_count = conn.execute('SELECT COUNT(*) FROM candidates').fetchone()[0]
    conn.close()
    
    ner_status = "<span style='color:#34D399;'>Online</span>" if nlp else "<span style='color:#F87171;'>Offline</span>"
    semantic_status = "<span style='color:#34D399;'>Active (MiniLM-L6)</span>" if embedding_model else "<span style='color:#F87171;'>Inactive</span>"
    
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card" style="border-top-color: #8B5CF6;">
            <div class="metric-title">🎯 Active Job Profiles</div>
            <div class="metric-value">{jobs_count}</div>
        </div>
        <div class="metric-card" style="border-top-color: #06B6D4;">
            <div class="metric-title">📄 Resumes Processed</div>
            <div class="metric-value">{cands_count}</div>
        </div>
        <div class="metric-card" style="border-top-color: #10B981;">
            <div class="metric-title">🔍 NER Extraction Engine</div>
            <div class="metric-value" style="font-size: 1.6rem;">{ner_status}</div>
        </div>
        <div class="metric-card" style="border-top-color: #F59E0B;">
            <div class="metric-title">🧠 Semantic Match Engine</div>
            <div class="metric-value" style="font-size: 1.6rem;">{semantic_status}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE 2: DATABASE & UPLOAD
# ==========================================
elif page == "⚙️ Database & Upload":
    st.markdown('<div class="main-title">Data Ingestion Center</div>', unsafe_allow_html=True)
    
    conn = get_db_connection()
    saved_jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Job Profile", "🗑️ Manage Database", "📤 Document Upload"])
    
    with tab1:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        with st.form("create_job_form", clear_on_submit=True):
            role = st.text_input("Job Title / Designation")
            skills = st.text_area("Required Skills (Comma separated)")
            col1, col2 = st.columns(2)
            exp = col1.number_input("Min Experience (Years)", 0, 20, 3)
            edu = col2.selectbox("Min Education", ["Bachelor's Degree", "Master's Degree", "PhD", "Any"])
            if st.form_submit_button("Inject into Database", type="primary"):
                if role and skills:
                    conn = get_db_connection()
                    conn.execute('INSERT INTO jobs (role_title, required_skills, min_experience, required_education) VALUES (?, ?, ?, ?)', (role, skills, exp, edu))
                    conn.commit()
                    conn.close()
                    st.success("✅ Job Profile successfully injected.")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        if saved_jobs:
            job_dict = {job['id']: job['role_title'] for job in saved_jobs}
            selected_job_id = st.selectbox("Select Profile to Drop:", options=list(job_dict.keys()), format_func=lambda x: job_dict[x])
            if st.button("Drop Profile", type="secondary"):
                conn = get_db_connection()
                conn.execute('DELETE FROM jobs WHERE id = ?', (selected_job_id,))
                conn.commit()
                conn.close()
                st.warning("Profile dropped from database.")
                st.rerun()
        else: st.info("Database is currently empty.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        options_list = ["🤖 AI Auto-Detect (ML Engine)"]
        if saved_jobs: options_list.extend([job['role_title'] for job in saved_jobs])
            
        target_job = st.selectbox("Target Pipeline Route:", options=options_list)
        st.markdown("---")
        
        uploaded_files = st.file_uploader("Upload Documents (.pdf, .docx, images)", type=['pdf', 'docx', 'png', 'jpg'], accept_multiple_files=True)
        
        if uploaded_files:
            if st.button("Execute Extraction Sequence", type="primary"):
                with st.spinner("Neural Engine mapping semantic vectors..."):
                    conn = get_db_connection()
                    success_count = 0
                    
                    for uploaded_file in uploaded_files:
                        text = extract_text_from_file(uploaded_file)
                        if not text or not text.strip(): continue
                        parsed = parse_resume(text, uploaded_file.name)
                        
                        final_job_role = target_job
                        req_skills_list = []
                        job_id_db = None
                        
                        if target_job == "🤖 AI Auto-Detect (ML Engine)":
                            inferred_title = role_classifier.predict([text])[0] if role_classifier else "General Candidate"
                            final_job_role = inferred_title
                            existing_job = conn.execute('SELECT * FROM jobs WHERE role_title = ?', (inferred_title,)).fetchone()
                            if existing_job:
                                req_skills_list = [s.strip().lower() for s in existing_job['required_skills'].split(',') if s.strip()]
                                job_id_db = existing_job['id']
                            else:
                                top_skills = ", ".join(list(parsed['skills'])[:6]) if parsed['skills'] else "General Technical Skills"
                                cursor = conn.execute('INSERT INTO jobs (role_title, required_skills, min_experience, required_education) VALUES (?, ?, ?, ?)', (inferred_title, top_skills, 0, "Any"))
                                job_id_db = cursor.lastrowid
                                req_skills_list = [s.strip().lower() for s in top_skills.split(',')]
                        else:
                            selected_job_data = conn.execute('SELECT * FROM jobs WHERE role_title = ?', (target_job,)).fetchone()
                            req_skills_list = [s.strip().lower() for s in selected_job_data['required_skills'].split(',')]
                            job_id_db = selected_job_data['id']

                        matched = []
                        missing = []
                        score = 0.0
                        
                        # ==========================================
                        # 🧠 THE NEW SEMANTIC MATCHING ENGINE
                        # ==========================================
                        if req_skills_list and parsed['skills']:
                            cand_skills_list = list(parsed['skills'])
                            
                            # Convert text into math vectors!
                            req_embeddings = embedding_model.encode(req_skills_list)
                            cand_embeddings = embedding_model.encode(cand_skills_list)
                            
                            # Calculate the angle between the word vectors
                            sim_matrix = cosine_similarity(req_embeddings, cand_embeddings)
                            
                            for i, req in enumerate(req_skills_list):
                                best_score = sim_matrix[i].max()
                                # If the words are mathematically 55% similar or higher, it's a match!
                                if best_score >= 0.55:  
                                    best_idx = sim_matrix[i].argmax()
                                    matched_term = cand_skills_list[best_idx]
                                    
                                    # If the words are different but the meaning is the same, show both!
                                    if req.lower() not in matched_term.lower() and matched_term.lower() not in req.lower():
                                        matched.append(f"{req.title()} (via {matched_term})")
                                    else:
                                        matched.append(req.title())
                                else:
                                    missing.append(req.title())
                                    
                            score = round((len(matched) / len(req_skills_list)) * 100, 1)
                        elif req_skills_list and not parsed['skills']:
                            missing = [req.title() for req in req_skills_list]
                        
                        conn.execute('''INSERT INTO candidates (job_id, job_role, name, email, phone, education, experience, skills, match_score, matched_skills, missing_skills) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (job_id_db, final_job_role, parsed['name'], parsed['email'], parsed['phone'], parsed['education'], parsed['experience'], json.dumps(parsed['skills']), score, json.dumps(matched), json.dumps(missing)))
                        success_count += 1
                    
                    conn.commit()
                    conn.close()
                    if success_count > 0: st.success(f"✅ {success_count} candidate profiles mapped to vector space and ingested.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 3: PIPELINE EXPLORER
# ==========================================
elif page == "👥 Candidate Pipeline":
    st.markdown('<div class="main-title">Candidate Pipeline</div>', unsafe_allow_html=True)
    
    conn = get_db_connection()
    roles_data = conn.execute('SELECT DISTINCT job_role FROM candidates').fetchall()
    roles = [row[0] for row in roles_data]
    
    if roles:
        col_filter, col_search = st.columns(2)
        with col_filter: filter_role = st.selectbox("🔎 Filter by Designation:", ["All Pipelines"] + roles)
        with col_search: search_name = st.text_input("👤 Search Candidate Database:")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        query = 'SELECT * FROM candidates WHERE 1=1'
        params = []
        if filter_role != "All Pipelines":
            query += ' AND job_role = ?'
            params.append(filter_role)
        if search_name:
            query += ' AND name LIKE ?'
            params.append(f'%{search_name}%')
        query += ' ORDER BY match_score DESC'
        
        candidates = conn.execute(query, params).fetchall()
        if not candidates: st.warning("No matches found in the current pipeline.")
        
        for cand in candidates:
            c_skills = json.loads(cand['skills'])
            c_matched = json.loads(cand['matched_skills'])
            c_missing = json.loads(cand['missing_skills'])
            
            st.markdown('<div class="dark-card">', unsafe_allow_html=True)
            
            col_profile, col_score = st.columns([3, 1])
            with col_profile:
                st.markdown(f"""
                <div class="profile-header">
                    <div class="avatar-box">👨‍💻</div>
                    <div>
                        <h3 class="cand-name">{cand["name"]}</h3>
                        <p class="cand-contact">📧 {cand["email"]} &nbsp;&nbsp;|&nbsp;&nbsp; 📱 {cand["phone"]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_score:
                badge_class = "score-high" if cand['match_score'] >= 80 else ("score-med" if cand['match_score'] >= 50 else "score-low")
                st.markdown(f'<div class="{badge_class}">{cand["match_score"]}% Match</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Drop Profile", key=f"del_{cand['id']}", use_container_width=True):
                    delete_candidate(cand['id'])
                    st.rerun()
            
            st.markdown(f"""
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-icon">🎓</div>
                    <div class="info-text-block">
                        <span class="info-label">Highest Education</span>
                        <span class="info-data">{cand['education']}</span>
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-icon">💼</div>
                    <div class="info-text-block">
                        <span class="info-label">Professional Experience</span>
                        <span class="info-data">{cand['experience']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # The UI will now display smart semantic matches!
            st.markdown('<div class="info-label" style="margin-bottom:8px;">✅ Semantically Verified Skills</div>', unsafe_allow_html=True)
            if c_matched: st.markdown("".join([f'<span class="pill-matched">{s}</span>' for s in c_matched]), unsafe_allow_html=True)
            else: st.caption("No semantic matches found.")
            
            st.markdown('<br><div class="info-label" style="margin-bottom:8px;">❌ Missing Requirements</div>', unsafe_allow_html=True)
            if c_missing: st.markdown("".join([f'<span class="pill-missing">{s}</span>' for s in c_missing]), unsafe_allow_html=True)
            else: st.caption("Candidate meets all semantic requirements.")
            
            with st.expander("View Raw Extracted Keyword Data"):
                st.markdown("".join([f'<span class="pill-neutral">{s}</span>' for s in c_skills]), unsafe_allow_html=True)
                    
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Pipeline is currently empty.")
    conn.close()
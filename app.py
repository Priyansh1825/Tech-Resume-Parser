import streamlit as st
import sqlite3

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Recruiter Pro", page_icon="💼", layout="wide")

# --- 2. ENTERPRISE CUSTOM CSS ---
# This hides Streamlit's default elements and adds modern SaaS styling
st.markdown("""
<style>
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Modern Typography & Background */
    .stApp {
        background-color: #F9FAFB;
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Headers */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #111827;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    
    /* Sleek Cards for Dashboard */
    .dashboard-card {
        background-color: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }
    
    /* Match Score Badges */
    .score-badge-high {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    .score-badge-med {
        background-color: #FEF08A;
        color: #854D0E;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    /* Custom Button Styling */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATABASE CONNECTION ---
def get_db_connection():
    conn = sqlite3.connect('ats_system.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("### 💼 AI Recruiter Pro")
    st.markdown("---")
    page = st.radio("Navigation Menu", ["🏠 Dashboard Home", "📝 Post a New Job", "👥 Candidate Pipeline"])
    st.markdown("---")
    st.caption("System Status: Online 🟢")

# ==========================================
# PAGE 1: DASHBOARD HOME
# ==========================================
if page == "🏠 Dashboard Home":
    st.markdown('<div class="main-title">Overview Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Monitor your open roles and candidate pipeline at a glance.</div>', unsafe_allow_html=True)
    
    # KPI Metrics Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Active Job Postings", value="3", delta="1 this week")
    with col2:
        st.metric(label="Total Resumes Processed", value="142", delta="24 today")
    with col3:
        st.metric(label="Highly Matched Candidates", value="12", delta="15% increase")
        
    st.markdown("---")
    
    st.markdown("### Quick Actions")
    action_col1, action_col2 = st.columns(2)
    with action_col1:
        st.info("**Need to hire?**\n\nCreate a new job requirement profile to start accepting applications.")
    with action_col2:
        st.success("**Review applicants?**\n\nHead to the Candidate Pipeline to see AI-ranked matches.")

# ==========================================
# PAGE 2: POST A NEW JOB
# ==========================================
elif page == "📝 Post a New Job":
    st.markdown('<div class="main-title">Create Job Requirement</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Define the ideal candidate profile and upload incoming resumes.</div>', unsafe_allow_html=True)
    
    col_form, col_upload = st.columns([1.5, 1])
    
    with col_form:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown("#### 1. Role Specifications")
        with st.form("job_form"):
            role = st.text_input("Job Title", placeholder="e.g., Senior Data Scientist")
            skills = st.text_area("Required Skills", placeholder="e.g., Python, TensorFlow, SQL, AWS...")
            
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                exp = st.number_input("Min. Experience (Years)", 0, 20, 3)
            with sub_col2:
                edu = st.selectbox("Minimum Education", ["Bachelor's Degree", "Master's Degree", "PhD", "Any"])
            
            submit_job = st.form_submit_button("Deploy Job Profile")
            if submit_job:
                st.toast("Job profile saved successfully!", icon="✅")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_upload:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown("#### 2. Bulk Resume Upload")
        st.write("Upload candidate CVs to match against this role.")
        uploaded_files = st.file_uploader("", type=['pdf', 'docx', 'png', 'jpg'], accept_multiple_files=True)
        
        if uploaded_files:
            if st.button("Extract & Match Candidates", use_container_width=True):
                with st.spinner("AI is reading and scoring resumes..."):
                    # We will put the NLP logic here later
                    st.success(f"Successfully processed {len(uploaded_files)} candidate(s)!")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 3: CANDIDATE PIPELINE
# ==========================================
elif page == "👥 Candidate Pipeline":
    st.markdown('<div class="main-title">Candidate Pipeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Review candidates automatically ranked by AI against your job requirements.</div>', unsafe_allow_html=True)
    
    # Filter Row
    st.selectbox("Filter by Job Role:", ["Senior Data Scientist", "Frontend Developer", "All Roles"])
    st.markdown("<br>", unsafe_allow_html=True)

    

    # --- Dummy Data for UI Mockup ---
    # We will replace this with real database queries later
    candidates = [
        {"name": "Alex Johnson", "score": 94, "skills": "Python, TensorFlow, SQL", "exp": "4 Years", "edu": "Master's Degree"},
        {"name": "Samantha Lee", "score": 88, "skills": "Python, React, Node.js", "exp": "3 Years", "edu": "Bachelor's Degree"},
        {"name": "Michael Chen", "score": 65, "skills": "Java, SQL", "exp": "1 Year", "edu": "Bachelor's Degree"}
    ]

    # Render Beautiful Candidate Cards
    for cand in candidates:
        badge_class = "score-badge-high" if cand["score"] > 80 else "score-badge-med"
        
        st.markdown(f"""
        <div class="dashboard-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h3 style="margin: 0; color: #1F2937;">{cand["name"]}</h3>
                <span class="{badge_class}">⭐ {cand["score"]}% AI Match</span>
            </div>
            <p style="color: #4B5563; margin-bottom: 5px;"><strong>Extracted Skills:</strong> {cand["skills"]}</p>
            <div style="display: flex; gap: 20px; color: #6B7280; font-size: 0.9rem;">
                <span>💼 {cand["exp"]}</span>
                <span>🎓 {cand["edu"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add an interactive expander native to Streamlit below each card
        with st.expander(f"View {cand['name']}'s Full AI Analysis"):
            st.write("Here we will show the exact overlapping skills, missing skills, and the raw text extracted from the CV.")
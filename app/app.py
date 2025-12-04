import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from math import pi

# Set page config
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

# Custom CSS to make images fill their containers
st.markdown("""
<style>
    /* Make images fill the entire column width */
    .stImage > img {
        width: 100% !important;
        height: auto !important;
        object-fit: contain;
    }
    /* Remove any padding around images */
    [data-testid="stImage"] {
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Try multiple path options (local vs Streamlit Cloud)
    possible_paths = [
        "../data/candidates.json",  # From app/ directory
        "data/candidates.json",      # From root directory
        "candidates.json"             # Same directory
    ]
    
    for path in possible_paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            continue
    
    st.error("candidates.json not found in any expected location. Please check repository structure.")
    return []

raw_data = load_data()

if not raw_data:
    st.stop()

# Convert to DataFrame for easier manipulation
df = pd.json_normalize(raw_data)
# Rename columns to remove 'skills.' prefix for easier access
df.columns = [c.replace('skills.', '') for c in df.columns]

# Helper to parse salary safely
def get_salary(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

df['parsed_salary'] = df['expected_net'].apply(get_salary)

# --- SIDEBAR ---
st.sidebar.header("⚙️ Controls")
uploaded_file = st.sidebar.file_uploader("Upload new CVs (PDF)", type="pdf", accept_multiple_files=True)
if uploaded_file:
    st.sidebar.info("Upload functionality is a placeholder in this demo. The agent has already processed existing files.")

st.sidebar.subheader("Filter Candidates")
min_c_score = st.sidebar.slider("Min C Programming Score", 0, 10, 0)
df_filtered = df[df['C_Programming'] >= min_c_score].copy()

# --- SCENARIO CALCULATION ---
def calculate_scores(row):
    # Scenario A: Startup Mode
    # 40% Culture (Soft) + 30% Generalist (Avg of C & Embedded) + 30% Agility (Leadership)
    generalist_tech = (row['C_Programming'] + row['Embedded_Systems']) / 2
    score_a = (0.4 * row['Soft_Skills']) + (0.3 * generalist_tech) + (0.3 * row['Leadership_Experience'])
    
    # Scenario B: Enterprise Mode
    # 50% Experience (Leadership) + 50% Specialized Hard Skills (Avg of C & Energy)
    specialized_hard = (row['C_Programming'] + row['Energy_Domain']) / 2
    score_b = (0.5 * row['Leadership_Experience']) + (0.5 * specialized_hard)
    
    return pd.Series([score_a, score_b], index=['Score_A_Startup', 'Score_B_Enterprise'])

df_filtered[['Score_A_Startup', 'Score_B_Enterprise']] = df_filtered.apply(calculate_scores, axis=1)

# --- MAIN LAYOUT ---
st.title("📊 HR Analytics: Candidate Intelligence Dashboard")

tab1, tab2, tab3 = st.tabs(["🏆 Leaderboard", "📈 Comparative Analysis", "🔍 Candidate Deep Dive"])

# --- TAB 1: LEADERBOARD ---
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚀 Scenario A: Startup Mode")
        st.markdown("*Weighted: 40% Culture, 30% Generalist, 30% Agility*")
        top_a = df_filtered.sort_values(by='Score_A_Startup', ascending=False)[['name', 'Score_A_Startup', 'status', 'avail_from']]
        st.dataframe(top_a.style.background_gradient(cmap='Greens', subset=['Score_A_Startup']), use_container_width=True)

    with col2:
        st.subheader("🏢 Scenario B: Enterprise Mode")
        st.markdown("*Weighted: 50% Experience, 50% Specialized Hard Skills*")
        top_b = df_filtered.sort_values(by='Score_B_Enterprise', ascending=False)[['name', 'Score_B_Enterprise', 'status', 'avail_from']]
        st.dataframe(top_b.style.background_gradient(cmap='Blues', subset=['Score_B_Enterprise']), use_container_width=True)

# --- TAB 2: COMPARATIVE ANALYSIS ---
with tab2:
    st.header("Comparative Visualizations")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Radar Chart: Core Competencies")
        categories = ['C_Programming', 'Embedded_Systems', 'Energy_Domain', 'Soft_Skills', 'Leadership_Experience']
        N = len(categories)
        
        # Radar Chart Implementation
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1] # Close the loop
        
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        
        # Limit to top 5 candidates to avoid clutter if list is long
        top_candidates = df_filtered.sort_values(by='Score_A_Startup', ascending=False).head(5)
        
        for i, row in top_candidates.iterrows():
            values = row[categories].tolist()
            values += values[:1] # Close the loop
            ax.plot(angles, values, linewidth=1, linestyle='solid', label=row['name'])
            ax.fill(angles, values, alpha=0.05)
        
        plt.xticks(angles[:-1], [c.replace('_', '\n') for c in categories], size=8)
        ax.set_rlabel_position(0)
        plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="grey", size=7)
        plt.ylim(0, 10)
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize='small')
        st.pyplot(fig)

    with c2:
        st.subheader("Salary vs. Startup Potential")
        
        # Scatter plot
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        
        # Filter out those without salary for the plot, or plot them as 0/Unknown? Better to filter.
        df_salary = df_filtered[df_filtered['parsed_salary'].notna()]
        
        if not df_salary.empty:
            sns.scatterplot(data=df_salary, x='parsed_salary', y='Score_A_Startup', hue='status', s=200, ax=ax2)
            
            # Annotate points
            for i, row in df_salary.iterrows():
                ax2.text(row['parsed_salary'], row['Score_A_Startup']+0.1, row['name'], fontsize=9)
                
            ax2.set_xlabel("Expected Net Salary (PLN)")
            ax2.set_ylabel("Startup Score (0-10)")
            ax2.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig2)
        else:
            st.info("No salary data available for the current selection to generate scatter plot.")

    st.divider()
    st.subheader("🔥 Skill Matrix Heatmap")
    
    # Create a matrix of specific skills from 'skills_list'
    # 1. Collect all unique skills
    all_skills = set()
    for skills in df_filtered['skills_list']:
        if isinstance(skills, list):
            for s in skills:
                all_skills.add(s)
    
    # 2. Filter to top N most common or relevant skills to avoid giant matrix
    # For now, let's pick some keywords of interest
    keywords = ["C", "Python", "Linux", "Modbus", "RTOS", "Embedded", "PCB", "TCP/IP", "SQL", "Git", "PLC", "SCADA"]
    
    matrix_data = []
    for i, row in df_filtered.iterrows():
        cand_skills = [s.lower() for s in row['skills_list']] if isinstance(row['skills_list'], list) else []
        row_data = {'Name': row['name']}
        for k in keywords:
            # Simple substring match
            present = any(k.lower() in s for s in cand_skills)
            row_data[k] = 1 if present else 0
        matrix_data.append(row_data)
        
    df_matrix = pd.DataFrame(matrix_data).set_index('Name')
    
    fig3, ax3 = plt.subplots(figsize=(10, len(df_filtered)*0.8 + 2))
    sns.heatmap(df_matrix, annot=True, cmap="Blues", cbar=False, linewidths=.5, ax=ax3)
    plt.xticks(rotation=45)
    st.pyplot(fig3)

# --- TAB 3: DEEP DIVE ---
with tab3:
    st.header("Candidate Dossiers")
    
    for i, row in df_filtered.iterrows():
        with st.expander(f"📄 {row['name']} (Status: {row['status']})"):
            
            # Display profile image at full width if available
            image_filename = row['name'].replace(" ", "_") + ".png"
            
            # Try multiple path options for images
            # Try multiple path options for images
            script_dir = os.path.dirname(os.path.abspath(__file__))
            possible_image_paths = [
                os.path.join(script_dir, "images", image_filename),      # app/images/
                os.path.join("images", image_filename),                  # Relative to CWD
                os.path.join("app", "images", image_filename),           # Relative to Root
                image_filename                                           # Fallback
            ]
            
            image_found = False
            for image_path in possible_image_paths:
                if os.path.exists(image_path):
                    # Display image filling the entire width
                    st.image(image_path, use_column_width=True, caption=row['name'])
                    image_found = True
                    break
            
            if not image_found:
                st.info("No profile image available")
            
            st.divider()
            
            # --- Header: Validation & Narrative ---
            if 'validation_status' in row and isinstance(row['validation_status'], dict):
                vs = row['validation_status']
                alignment = vs.get('alignment', '')
                justification = vs.get('justification', '')
                if alignment or justification:  # Only show if not empty
                    st.info(f"**Alignment:** {alignment or 'N/A'} - {justification}")
            
            if 'bigger_picture_narrative' in row and isinstance(row['bigger_picture_narrative'], dict):
                bp = row['bigger_picture_narrative']
                persona = bp.get('persona', '')
                narrative = bp.get('narrative', '')
                culture_fit = bp.get('culture_fit', '')
                
                if persona:
                    st.markdown(f"**Persona:** `{persona}`")
                if narrative:
                    st.markdown(f"_{narrative}_")
                if culture_fit:
                    st.caption(f"**Culture Fit:** {culture_fit}")
            
            st.divider()

            c1, c2 = st.columns(2)
            with c1:
                # Gap Analysis
                has_gap = False
                if 'gap_analysis_detailed' in row and isinstance(row['gap_analysis_detailed'], list) and row['gap_analysis_detailed']:
                    has_gap = True
                elif row.get('gap_analysis'):
                    has_gap = True
                
                if has_gap:
                    st.markdown("**Gap Analysis:**")
                    if 'gap_analysis_detailed' in row and isinstance(row['gap_analysis_detailed'], list) and row['gap_analysis_detailed']:
                        for gap in row['gap_analysis_detailed']:
                            st.markdown(f"- {gap}")
                    else:
                        st.write(row['gap_analysis'])
                
                # Availability
                avail = row.get('avail_from')
                if avail and avail not in ["N/A", "-", ""]:
                    st.markdown(f"**Availability:** {avail}")
                
                # Salary
                salary = row.get('expected_net')
                if salary and salary not in ["N/A", "-", ""]:
                    st.markdown(f"**Expected Net:** {salary}")
                
            with c2:
                # Search Findings
                findings = row.get('search_findings')
                if findings and findings not in ["N/A", ""]:
                    st.markdown("**Search Findings:**")
                    st.write(findings)
                
                # Experience Similar
                exp_sim = row.get('exp_similar')
                if exp_sim and exp_sim not in ["N/A", "-", ""]:
                    st.markdown(f"**Experience Similar:** {exp_sim}")
                
                # Interview Strategy
                if 'interview_strategy' in row and isinstance(row['interview_strategy'], list) and row['interview_strategy']:
                    st.markdown("**Suggested Interview Questions:**")
                    for q in row['interview_strategy']:
                        st.markdown(f"- {q}")
            
            st.markdown("---")
            st.subheader("Skills & Attributes")
            
            # Display boolean attributes as tags
            attrs = {
                "Energy Exp": row.get('energy_experience'),
                "OZE Exp": row.get('OZE_experience'),
                "Modbus": row.get('modbus'),
                "Linux": row.get('linux'),
                "C Lang": row.get('c_language'),
                "Git": row.get('git')
            }
            
            tags = [k for k, v in attrs.items() if v]
            if tags:
                st.write("Verified Tags: " + ", ".join([f"`{t}`" for t in tags]))
            
            if 'skills_list' in row and isinstance(row['skills_list'], list) and row['skills_list']:
                 st.write("Skills List: " + ", ".join(row['skills_list']))
            
            if 'comment' in row and row['comment']:
                st.info(f"**Comment:** {row['comment']}")

            st.markdown("---")
            st.caption("Raw Skills Data:")
            st.json(row[categories].to_dict())


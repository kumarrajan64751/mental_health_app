
import streamlit as st
from streamlit_lottie import st_lottie
import json
import pickle
import pandas as pd
from report_generator import generate_pdf_report
from google.oauth2 import service_account
import gspread
from datetime import datetime
import os

# ✅ Set page config FIRST
st.set_page_config(page_title="Student Mental Health Predictor", layout="centered")


st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* Background and base text color */
    html, body, .stApp {
        background-color: #cceeff;
        color: #000000 !important;
        font-size: 18px !important; /* Increase base font size */
    }

    /* Set width of main container */
    .main .block-container {
        max-width: 1000px;
        padding: 2rem;
        margin: auto;
    }

    /* Make all headings and paragraphs black and larger */
    h1, h2, h3, h4, h5, h6, p, label, span, div, textarea {
        color: #000000 !important;
        font-size: 1.1rem !important;
    }

    /* Increase size of slider labels specifically */
    label.css-15tx938, label[data-testid="stFormLabel"] {
        font-size: 1.2rem !important;
        color: #000000 !important;
    }

    /* Style normal buttons */
    .stButton>button {
        background-color: #5dade2;
        color: white !important;
        font-size: 1rem !important;
        padding: 0.5rem 1rem;
    }

    /* Style download button */
    .stDownloadButton>button {
        background-color: #45b39d;
        color: white !important;
        font-size: 1rem !important;
        padding: 0.5rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Load Lottie animation ---
def load_lottie_animation(path: str):
    with open(path, "r") as f:
        return json.load(f)

lottie_animation = load_lottie_animation("lottie_animation.json")

# --- Title and Animation ---
st_lottie(lottie_animation, height=200)
st.title("🧠 Mental Health Predictor for Students")

# --- User Input ---
name = st.text_input("👤 Enter your Name")

if not name:
    st.warning("⚠️ Please enter your name to begin.")
    st.stop()

# --- Model Load ---
dep_model = pickle.load(open("depression_model.pkl", "rb"))
anx_model = pickle.load(open("anxiety_model.pkl", "rb"))
stress_model = pickle.load(open("stress_model.pkl", "rb"))

# --- Question Texts ---
phq_questions = [
    "Little interest or pleasure in doing things",
    "Feeling down, depressed, or hopeless",
    "Trouble falling or staying asleep, or sleeping too much",
    "Feeling tired or having little energy",
    "Poor appetite or overeating",
    "Feeling bad about yourself — or that you are a failure or have let yourself or your family down",
    "Trouble concentrating on things, such as reading or watching TV",
    "Moving or speaking so slowly that other people could have noticed — or the opposite, being fidgety or restless",
    "Thoughts that you would be better off dead, or thoughts of hurting yourself"
]

gad_questions = [
    "Feeling nervous, anxious or on edge",
    "Not being able to stop or control worrying",
    "Worrying too much about different things",
    "Trouble relaxing",
    "Being so restless that it is hard to sit still",
    "Becoming easily annoyed or irritable",
    "Feeling afraid as if something awful might happen"
]

epw_questions = [
    "I found it hard to wind down",
    "I tended to over-react to situations",
    "I felt that I was using a lot of nervous energy",
    "I found myself getting agitated",
    "I found it difficult to relax",
    "I was intolerant of anything that kept me from getting on with what I was doing",
    "I felt that I was rather touchy",
    "I was aware of dryness of my mouth"
]

# --- Answer labels ---
phq_gad_options = {
    "Not at all": 0,
    "Several days": 1,
    "More than half the days": 2,
    "Nearly every day": 3
}

epw_options = {
    "Did not apply to me at all": 1,
    "Applied to me to some degree": 2,
    "Applied to me to a considerable degree": 3,
    "Applied to me very much": 4
}

# --- Input Features ---
st.subheader("📋 Answer the following survey:")

phq_scores = []
for i, q in enumerate(phq_questions):
    response = st.radio(f"PHQ{i+1} - {q}", list(phq_gad_options.keys()), index=0, key=f"phq{i}")
    phq_scores.append(phq_gad_options[response])

gad_scores = []
for i, q in enumerate(gad_questions):
    response = st.radio(f"GAD{i+1} - {q}", list(phq_gad_options.keys()), index=0, key=f"gad{i}")
    gad_scores.append(phq_gad_options[response])

epw_scores = []
for i, q in enumerate(epw_questions):
    response = st.radio(f"EPW{i+1} - {q}", list(epw_options.keys()), index=0, key=f"epw{i}")
    epw_scores.append(epw_options[response])


if st.button("🧪 Predict My Mental Health"):
    data = pd.DataFrame([phq_scores + gad_scores + epw_scores])
    depression_pred = dep_model.predict(data)[0]
    anxiety_pred = anx_model.predict(data)[0]
    stress_pred = stress_model.predict(data)[0]

    st.success("✅ Prediction Complete")

    st.subheader("Your Mental Health Summary")
    st.write(f"**Depression Level:** {depression_pred}")
    st.write(f"**Anxiety Level:** {anxiety_pred}")
    st.write(f"**Stress Level:** {stress_pred}")

    # Generate and offer PDF download
    report_name = f"{name.replace(' ', '_')}_mental_health_report.pdf"
    output_path = os.path.join( report_name)
    phq_qas = [(phq_questions[i], list(phq_gad_options.keys())[list(phq_gad_options.values()).index(score)]) for i, score in enumerate(phq_scores)]
    gad_qas = [(gad_questions[i], list(phq_gad_options.keys())[list(phq_gad_options.values()).index(score)]) for i, score in enumerate(gad_scores)]
    epw_qas = [(epw_questions[i], list(epw_options.keys())[list(epw_options.values()).index(score)]) for i, score in enumerate(epw_scores)]
    generate_pdf_report(
        name,
        phq_qas,
        gad_qas,
        epw_qas,
        sum(phq_scores),
        sum(gad_scores),
        sum(epw_scores),
        depression_pred,
        anxiety_pred,
        stress_pred,
        output_path
    )
    with open(output_path, "rb") as f:
        st.download_button(
            label="Download Your PDF Report",
            data=f,
            file_name=report_name,
            mime="application/pdf"
        )

    # Optional links after prediction
    st.markdown("---")
    st.subheader("🌱 Further Support & Guidance")
    st.markdown(
        """
        🔗 [**Try Guided Mindfulness Exercises**](https://kumarrajan64751.github.io/Mindfulness-and-mental-Wellness/)  
        🩺 [**Connect With a Mental Health Professional**](https://www.psychologytoday.com/us/therapists)
        """,
        unsafe_allow_html=True
    )

    # Retake button
    if st.button("🔄 Retake Test"):
        st.experimental_rerun()


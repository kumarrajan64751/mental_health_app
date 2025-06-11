from fpdf import FPDF

def clean_text(text):
    """Replace or remove characters that fpdf cannot encode (non-latin-1)."""
    replacements = {
        "—": "-", "–": "-",
        "“": '"', "”": '"',
        "‘": "'", "’": "'",
        "…": "..."
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text.encode("latin-1", "ignore").decode("latin-1")

def generate_pdf_report(name, phq_qas, gad_qas, epw_qas, phq_score, gad_score, epw_score,
                        depression_pred, anxiety_pred, stress_pred, output_path):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, clean_text("Student Mental Health Report"), ln=True)

    # Name
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, clean_text(f"Name: {name}"), ln=True)
    pdf.ln(5)

    # PHQ-9 Responses
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, clean_text("PHQ-9 Responses:"), ln=True)
    pdf.set_font("Arial", "", 12)
    for question, answer in phq_qas:
        pdf.multi_cell(0, 10, clean_text(f"{question} - {answer}"))

    # GAD-7 Responses
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, clean_text("GAD-7 Responses:"), ln=True)
    pdf.set_font("Arial", "", 12)
    for question, answer in gad_qas:
        pdf.multi_cell(0, 10, clean_text(f"{question} - {answer}"))

    # EPW Responses
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, clean_text("EPW Responses:"), ln=True)
    pdf.set_font("Arial", "", 12)
    for question, answer in epw_qas:
        pdf.multi_cell(0, 10, clean_text(f"{question} - {answer}"))

    # Scores
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, clean_text("Total Scores:"), ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, clean_text(f"PHQ-9 Total Score: {phq_score}"), ln=True)
    pdf.cell(0, 10, clean_text(f"GAD-7 Total Score: {gad_score}"), ln=True)
    pdf.cell(0, 10, clean_text(f"EPW Total Score: {epw_score}"), ln=True)

    # Predictions
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, clean_text("Predicted Mental Health Levels:"), ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, clean_text(f"Depression Level: {depression_pred}"), ln=True)
    pdf.cell(0, 10, clean_text(f"Anxiety Level: {anxiety_pred}"), ln=True)
    pdf.cell(0, 10, clean_text(f"Stress Level: {stress_pred}"), ln=True)

    # Save PDF
    pdf.output(output_path)



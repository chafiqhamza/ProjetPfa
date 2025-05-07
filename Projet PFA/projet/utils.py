from docx import Document
import PyPDF2
import openai

# Extract text
def extract_text_from_pdf(path):
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return "\n".join(p.extract_text() or '' for p in reader.pages)

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

# SWOT analysis (basic)
def generate_swot_analysis(text):
    strengths, weaknesses, opportunities, threats = [], [], [], []
    if any(k in text for k in ['python','java']): strengths.append('Strong coding skills')
    if 'cloud' not in text: weaknesses.append('Limited cloud experience')
    if 'machine learning' in text: opportunities.append('AI/ML demand')
    threats.append('Competitive market')
    return {"Strengths": strengths, "Weaknesses": weaknesses,
            "Opportunities": opportunities, "Threats": threats}

# Query LLM
def query_llm(prompt):
    openai.api_key = "your_openai_api_key_here"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Summarize job description
def summarize_job_description(description):
    prompt = f"Summarize the following job description:\n{description}"
    return query_llm(prompt)
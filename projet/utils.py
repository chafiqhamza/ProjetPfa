from docx import Document
import PyPDF2
import openai


# Mock the OpenAI API
def mock_openai_api():
    class MockResponse:
        def __init__(self, content):
            self.content = content

        def __getitem__(self, key):
            if key == "choices":
                return [{"message": {"content": self.content}}]
            raise KeyError(key)

    def mock_chat_completion_create(*args, **kwargs):
        return MockResponse("Strengths: Strong programming skills\nWeaknesses: Limited experience in cloud computing\nOpportunities: High demand for software engineers\nThreats: Competitive job market")

    openai.ChatCompletion.create = mock_chat_completion_create

mock_openai_api()

# Extract text
def extract_text_from_pdf(path):
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return "\n".join(p.extract_text() or '' for p in reader.pages)

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

# Enhanced SWOT analysis function to provide more detailed insights
def generate_swot_analysis(text):
    """
    Generate a SWOT analysis dynamically using AI based on the provided text.
    """
    prompt = (
        f"Analyze the following CV text and provide a detailed SWOT analysis (Strengths, Weaknesses, Opportunities, Threats):\n\n"
        f"CV Text:\n{text}\n\n"
        f"Provide actionable and specific insights for each category."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        # Parse the AI response
        swot_analysis = response["choices"][0]["message"]["content"].strip()

        # Split the response into categories
        swot_sections = swot_analysis.split("\n")
        swot_dict = {"Strengths": [], "Weaknesses": [], "Opportunities": [], "Threats": []}

        for section in swot_sections:
            if section.startswith("Strengths:"):
                swot_dict["Strengths"] = section.replace("Strengths:", "").strip().split("\n")
            elif section.startswith("Weaknesses:"):
                swot_dict["Weaknesses"] = section.replace("Weaknesses:", "").strip().split("\n")
            elif section.startswith("Opportunities:"):
                swot_dict["Opportunities"] = section.replace("Opportunities:", "").strip().split("\n")
            elif section.startswith("Threats:"):
                swot_dict["Threats"] = section.replace("Threats:", "").strip().split("\n")

        return swot_dict

    except Exception as e:
        # Provide fallback data
        return {
            "Strengths": ["Unable to generate strengths due to an error."],
            "Weaknesses": ["Unable to generate weaknesses due to an error."],
            "Opportunities": ["Unable to generate opportunities due to an error."],
            "Threats": ["Unable to generate threats due to an error."],
            "Error": str(e)
        }

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

# Dynamic SWOT analysis
def generate_dynamic_swot_analysis(cv_text, comparison_cvs):
    """Generate a dynamic SWOT analysis for a CV using AI-powered tools."""
    openai.api_key = "your_openai_api_key_here"

    # Combine the CV text with comparison CVs for context
    prompt = (
        f"Analyze the following CV and provide a SWOT analysis (Strengths, Weaknesses, Opportunities, Threats):\n\n"
        f"CV to analyze:\n{cv_text}\n\n"
        f"Comparison CVs:\n{comparison_cvs}\n\n"
        f"Provide a detailed SWOT analysis based on the comparison."
    )

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )

    return response.choices[0].text.strip()
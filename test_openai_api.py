import openai

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

# Mock the OpenAI API
mock_openai_api()

def test_openai_api():
    prompt = "Provide a SWOT analysis for a software engineer CV."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        print("API Response:")
        print(response["choices"][0]["message"]["content"].strip())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_openai_api()

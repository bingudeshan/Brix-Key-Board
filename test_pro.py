import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_pro_quota():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel("gemini-pro")
    prompt = "Translate Singlish to natural English: Mama adha gedhara enna na"
    
    print("Testing gemini-pro...")
    try:
        response = model.generate_content(prompt)
        print(f"Result: {response.text.strip()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_pro_quota()

import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_model_2_0():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # Try the 2.0 flash model
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = "Translate Singlish to natural English: Mama adha gedhara enna na"
    
    print("Testing gemini-2.0-flash...")
    try:
        response = model.generate_content(prompt)
        print(f"Result: {response.text.strip()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_model_2_0()

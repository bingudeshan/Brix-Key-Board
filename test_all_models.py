import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_models():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found")
        return
    
    genai.configure(api_key=api_key)
    
    # Test different model names
    models_to_test = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro",
        "gemini-pro",
    ]
    
    system_instruction = (
        "You are a Singlish-to-English translator. "
        "Convert phonetic Sinhala to English. "
        "Example: 'amma' -> 'Mother'. "
        "Provide only the direct translation."
    )
    
    test_text = "amma"
    
    print("Searching for working Gemini Models...\n")
    
    for model_name in models_to_test:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
            response = model.generate_content(test_text)
            print(f"SUCCESS {model_name}: {response.text.strip()}")
        except Exception as e:
            print(f"FAILED {model_name}: {str(e)[:100]}")

if __name__ == "__main__":
    test_models()

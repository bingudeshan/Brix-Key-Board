import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_translation():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file.")
        return

    print("Initializing Gemini...")
    genai.configure(api_key=api_key)
    
    system_instruction = (
        "You are a strict Singlish-to-English translator. "
        "Convert phonetic Sinhala (Singlish) to natural, gramatically correct English. "
        "Example: 'Mata bada gini' -> 'I am hungry'. "
        "Do not add any conversational filler, explanations, or notes. Just provide the direct translation."
    )
    
    # Use gemini-1.5-flash for translation
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )
    
    test_phrases = ["amma", "kohomada", "sthuthi", "mata bada gini"]
    
    print("\n--- Testing Transliteration ---")
    for phrase in test_phrases:
        try:
            response = model.generate_content(phrase)
            print(f"Input: {phrase} -> Output: {response.text.strip()}")
        except Exception as e:
            print(f"Error for '{phrase}': {str(e)}")

if __name__ == "__main__":
    test_translation()

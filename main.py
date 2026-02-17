import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI(
    title="Brix Keyboard AI Translation Service",
    description="FastAPI microservice for Singlish-to-English translation using Gemini 1.5 Flash",
    version="1.0.0"
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class TranslationRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    translated_text: str

# Enhanced System Instruction for Gemini
SYSTEM_INSTRUCTION = (
    "You are an expert Singlish (Sinhala-English phonetic) to natural English translator with deep understanding of Sri Lankan culture and Sinhala grammar.\n\n"
    
    "LINGUISTIC CONTEXT:\n"
    "- Sinhala uses Subject-Object-Verb (SOV) word order, but Singlish often mixes this with English SVO patterns\n"
    "- Common colloquialisms: 'mis' = teacher/miss (not mistake), 'machan' = friend/bro, 'aiyo' = oh no/oops\n"
    "- Negation patterns: 'na'/'ne' at end = negative, 'epa' = don't want\n"
    "- Question markers: '-da' suffix indicates questions, 'neda' = isn't it?\n"
    "- Politeness: 'karunakara' = please, '-ko' suffix adds politeness\n\n"
    
    "TRANSLATION RULES:\n"
    "1. Produce ONLY natural, conversational English - no literal word-by-word translations\n"
    "2. Understand context: 'adha' in different positions can mean 'today' or be emphatic\n"
    "3. Handle mixed scripts: Singlish words mixed with English should flow naturally\n"
    "4. Preserve intent: informal → informal, polite → polite\n"
    "5. Fix word order: Convert SOV patterns to natural English SVO\n\n"
    
    "FEW-SHOT EXAMPLES:\n"
    "Input: 'mama adha gedhara yanna ona na'\n"
    "Output: I don't need to go home today\n\n"
    
    "Input: 'oya kohomada adha'\n"
    "Output: How are you today?\n\n"
    
    "Input: 'api bath kanawa'\n"
    "Output: We're eating rice\n\n"
    
    "Input: 'mis mama balannam'\n"
    "Output: Miss, I'll take a look\n\n"
    
    "Input: 'dan oya mama type karana Singlish wachan therum gannwa wage'\n"
    "Output: Now, understand the Singlish words I'm typing just like you do\n\n"
    
    "CRITICAL: Respond with ONLY the English translation. No explanations, no notes, no conversational responses."
)

# Local quota saver for common phrases
LOCAL_QUOTA_SAVER = {
    "sthuthi": "Thank you",
    "ayubowan": "Hello",
    "hari": "Yes/Okay",
    "ne": "No",
    "na": "No",
}

def pre_process_translation(text: str) -> str:
    """Simple local mapping for very common Singlish phrases to save quota."""
    cleaned = text.lower().strip()
    if cleaned in LOCAL_QUOTA_SAVER:
        return LOCAL_QUOTA_SAVER[cleaned]
    return ""

# Initialize Gemini Model
def get_model():
    # UPDATED: Use gemini-flash-latest which appeared in user's model list
    return genai.GenerativeModel(
        model_name="gemini-flash-latest",
        system_instruction=SYSTEM_INSTRUCTION
    )

@app.get("/")
async def root():
    return {"message": "Brix Keyboard AI Translation Service is running."}

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Translates Singlish text to English using Gemini 1.5 Flash.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key is not configured")

    try:
        # 1. Check local quota saver first
        local_result = pre_process_translation(request.text)
        if local_result:
            print(f"Quota saved! Local translation: {local_result}")
            return TranslationResponse(translated_text=local_result)

        # 2. Try multiple models as fallbacks
        models_to_try = ["gemini-flash-latest", "gemini-2.0-flash", "gemini-pro-latest"]
        last_error = ""

        print(f"Translating: {request.text}")
        
        for model_name in models_to_try:
            try:
                print(f"Trying model: {model_name}...")
                model = genai.GenerativeModel(model_name=model_name, system_instruction=SYSTEM_INSTRUCTION)
                response = model.generate_content(request.text)
                
                if response.text:
                    print(f"Success with {model_name}: {response.text.strip()}")
                    return TranslationResponse(translated_text=response.text.strip())
            except Exception as e:
                last_error = str(e)
                print(f"Error with {model_name}: {last_error}")
                continue
        
        # If all models failed
        raise HTTPException(status_code=500, detail=f"All Gemini models failed. Last error: {last_error}")
        
    except Exception as e:
        print(f"Final Translation Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Starting Brix AI Backend...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

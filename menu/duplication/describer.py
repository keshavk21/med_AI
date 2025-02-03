import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=google_api_key)

# Define system prompt
system_prompt_tdd ={"text":"""You are a medical AI Agent.Tell is there any theraputic duplication in the list in 100 words"""}

# Function to call Gemini API
def message_gemini(user_prompt):
    try:
        gemini = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction=system_prompt_tdd)
        response = gemini.generate_content(user_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return "Error"

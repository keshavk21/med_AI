import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=google_api_key)

# Define system prompt
system_prompt_dfc ={"text":"""You are a medical AI Agent. Classify on the bases:
                1.Major:Highly clinically significant. Avoid combinations; the risk of the interaction outweighs the benefit.
                2.Moderate:Moderately clinically significant. Usually avoid combinations; use it only under special circumstances.
                3.Minor:Minimally clinically significant. Minimize risk; assess risk and consider an alternative drug, take steps to circumvent the interaction risk and/or institute a monitoring plan in 1 word"""}

# Function to call Gemini API
def message_gemini(user_prompt):
    try:
        gemini = genai.GenerativeModel("gemini-1.5-flash",
        system_instruction=system_prompt_dfc)
        response = gemini.generate_content(user_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return "Error"

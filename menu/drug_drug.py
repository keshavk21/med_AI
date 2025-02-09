from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

system_prompt = """You are a medical AI agent. Classify drug interactions as Major, Moderate, or Minor.
    Where:
        1. Major: High clinical risk. Avoid combination; risks outweigh benefits.
        2. Moderate: Moderate risk. Avoid unless necessary; use with caution.
        3. Minor: Low risk. Minimize risk through alternatives, precautions, or monitoring.

Describe the reaction between to the above drugs to human, in 100 words.
Format :
{
	"drug_classification": "(Major, Moderate, or Minor)",
	"drug_description" : "description"
}
"""

def stream_output(user_prompt):
    try:
        chat_completion = client.chat.completions.create(

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],

        model="llama-3.3-70b-versatile",
        temperature=1,
        top_p=0.2,
        stop=None,
        stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error with AI API: {e}")
        return "error"

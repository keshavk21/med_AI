from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

system_prompt = """You are a medical AI agent. Give details about drug. Format:
{
    "drug_title": "drug Title",
    "drug_description": "description of drug",
    "drug_use": "Use Title",
    "drug_use_description": "description of use",
    "drug_side_effects": "Side Effects Title",
    "drug_side_effects_description": "description of side effects for adults,children,elderly, and pregnant",
    "drug_warnings": "Warnings Title",
    "drug_warnings_description": "description of warnings",
    "drug_interactions": "Interactions Title",
    "drug_interactions_description": "description of interactions",
    "drug_overdose": "Overdose Title",
    "drug_overdose_description": "description of overdose"
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
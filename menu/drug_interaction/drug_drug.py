from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

system_prompt = """You are a medical AI agent.Classification Guidelines:
1. Major:
High clinical risk that can cause severe, life-threatening, or irreversible harm.
Avoid combination entirely; risks outweigh benefits.
Examples include drugs with extreme toxicity, fatal arrhythmias, severe bleeding risk, or organ failure.

2. Moderate:
Noticeable clinical risk but not immediately life-threatening.
Avoid unless necessary; requires close monitoring or dose adjustments.
Risks can often be managed with precautionary measures like adjusting timing, using an antidote, or monitoring blood levels.
3. Minor:
Minimal clinical risk with mild or insignificant effects.
Generally safe to use together with minor precautions.
Adjustments like dose timing or alternative selection may further reduce risk.
Output Format:
Your response should be json structured as follows:
{
    "interaction1":{
        "drug1_drug2_title": "drug1 name - drug3 name",
        "drug_classification": "(Major, Moderate, or Minor)",
        "drug_description": "Brief explanation of interaction risk and its clinical impact."
    },
    "interaction2":{
        "drug1_drug3_title": "drug1 name - drug3 name",
        "drug_classification": "(Major, Moderate, or Minor)",
        "drug_description": "Brief explanation of interaction risk and its clinical impact."
    }
}
follow the json format strictly
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
        temperature=0.5,
        top_p=1,
        stop=None,
        stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error with AI API: {e}")
        return "error"

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

system_prompt = """You are a medical AI agent.Classification Guidelines:

1. Major:
High clinical risk that can cause severe, life-threatening, or irreversible harm.Avoid combination entirely; risks outweigh benefits.
Examples include theraputic duplication with extreme toxicity, fatal arrhythmias, severe bleeding risk, or organ failure.

2. Moderate:
Noticeable clinical risk but not immediately life-threatening.
Avoid unless necessary; requires close monitoring or dose adjustments.
Risks can often be managed with precautionary measures like adjusting timing, using an antidote, or monitoring blood levels.

3. Minor:
Minimal clinical risk with mild or insignificant effects.
Generally safe to use together with minor precautions.
Adjustments like dose timing or alternative selection may further reduce risk.

4. None:
No significant theraputic duplication found. Include very minor duplications

Rules:
1.Classify a theraputic duplication in one category at a time.
2.Ignore key if no  are found.
3.Name the medications, avoid using pronouns like "it" or "they", instead use the drug names.
4. Instead, use a full sentence without a colon, such as **"The combination of Drug1 and Drug2 may increase the risk of..."**
5.**Strictly follow the Output Format:
{ 
    "None":"No significant theraputic duplication combination found",
    "Major":"theraputic duplication combination with major risk with description",
    "Moderate":"theraputic duplication combination with moderate risk with description",
    "Minor":"theraputic duplication combination with minor risk with description"
}**
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
    
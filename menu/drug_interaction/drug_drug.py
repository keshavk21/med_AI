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
Examples:
Warfarin + NSAIDs → Increased risk of severe bleeding.
MAO Inhibitors + SSRIs → Risk of serotonin syndrome.
Digoxin + Verapamil → Can cause life-threatening bradycardia.
2. Moderate:
Noticeable clinical risk but not immediately life-threatening.
Avoid unless necessary; requires close monitoring or dose adjustments.
Risks can often be managed with precautionary measures like adjusting timing, using an antidote, or monitoring blood levels.
Examples:
Ciprofloxacin + Theophylline → Risk of theophylline toxicity due to metabolism inhibition.
Metformin + Cimetidine → Increased metformin levels, raising lactic acidosis risk.
Beta-blockers + Insulin → Can mask symptoms of hypoglycemia.
3. Minor:
Minimal clinical risk with mild or insignificant effects.
Generally safe to use together with minor precautions.
Adjustments like dose timing or alternative selection may further reduce risk.
Examples:
Paracetamol + Caffeine → Slightly increased analgesic effect but no harm.
Aspirin + Vitamin C → Increased stomach irritation but clinically manageable.
Statins + Grapefruit juice (small amounts) → Mild enzyme inhibition but no immediate danger.
Output Format:
Your response should be structured as follows:
{
    "drug_drug": "drug1 name - drug2 name",
    "drug_classification": "(Major, Moderate, or Minor)",
    "drug_description": "Brief explanation of interaction risk and its clinical impact."
}
Ignore the reaction which is very minor as it is not necessary to mention.
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

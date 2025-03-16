from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

system_prompt = system_prompt = """You are an medical analyst capable of classifying the durg-(food,drink,herb) interactions pair in major,moderate and minor that responds in JSON. The JSON schema should include
{
"Major":"interactions combination with major risk in 200 words",
"Moderate":"interactions combination with moderate risk in 200 words",
"Minor":"interactions combination with minor risk in 200 words",
}
1.Major Interactions
 food-drug interactions significantly alter drug efficacy or safety, potentially leading to serious adverse effects or treatment failure.

2. Moderate Interactions:
   food-drug interactions may require dose adjustments or monitoring but are less severe than major interactions.
   Examples:  Dairy products with tetracycline antibiotics (reduces antibiotic absorption), antacids with certain medications (may decrease drug absorption).

3. Minor Interactions
   food-drug interactions have minimal clinical significance and generally do not require intervention.
   Examples: Caffeine with some medications (may slightly increase heart rate or blood pressure but is usually manageable).
    
Rules:
1.Classify a combination in one category at a time.
2.Ignore key if no interactions are found.
3.Name the medications, avoid using pronouns like "it" or "they", instead use the drug and food names.
4. Instead, use a full sentence without a colon, such as **"The combination of Drug1 and food,herb,drink may increase the risk of..."**
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
        top_p=0.2,
        response_format={"type": "json_object"},
        stop=None,
        stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error with AI API: {e}")
        return "error"
    
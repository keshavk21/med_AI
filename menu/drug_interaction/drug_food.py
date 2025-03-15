from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

system_prompt = system_prompt = """You are a medical AI agent that check that interaction of food/drink/herb with drugs in Markdown. Classification guidelines:
**Always Strictly follow the Output Format:
{ 
    "None":"No significant food/drink/herb combination found",
    "Major":"food/drink/herb combination with major risk with description",
    "Moderate":"food/drink/herb combination with moderate risk with description",
    "Minor":"food/drink/herb combination with minor risk with description"
}**

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
        stop=None,
        stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error with AI API: {e}")
        return "error"
    
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

system_prompt = system_prompt = """You are an medical analyst capable of classifying the durg-food,drink,herb interactions pairs in major,moderate and minor that responds in JSON. The JSON schema should include
{
"Major":"drug-food/drink/herb interactions combination with major risk in 200 words",
"Moderate":"food/drink/herb interactions combination with moderate risk in 200 words",
"Minor":"food/drink/herb interactions combination with minor risk in 200 words",
"No Interaction": "no food/drink/herb interactions found"
}

Rules:
1.Ignore key if no interactions are found.
2.Name the medications, avoid using pronouns like "it" or "they", instead use the drug and food names.
3. Instead, use a full sentence without a colon, such as **"The combination of Drug1 and food,herb,drink may increase the risk of..."**
4. Do **not** show durg-drug interactions and drug risk. 
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
    
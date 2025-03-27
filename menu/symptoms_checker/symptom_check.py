from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

system_prompt = """You are a medical AI agent. you need to give only names possible medical conditions or possible causes based on the symptoms,gender,age and country provided by the user in JSON format:
{
    condition_1:first condition name,
    condition_2:second condition name,
    condition3_3:third condition name,
    # Include as many medical condition as you think in decreasing order of probability
}
give atleast 10 results
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
        response_format={"type": "json_object"},
        stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error with AI API: {e}")
        return "error"
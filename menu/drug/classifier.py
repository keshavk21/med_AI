from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
) 

# Define system prompt
system_prompt_ddc = """You are a medical AI agent. Classify the interaction of drugs into one of these categories:
                1. Major: Highly clinically significant. Avoid combinations; the risk outweighs the benefit.
                2. Moderate: Moderately clinically significant. Usually avoid combinations; use only under special circumstances.
                3. Minor: Minimally clinically significant. Minimize risk; assess risk and consider an alternative drug, take steps to circumvent interaction risk, and/or institute a monitoring plan.
                Respond with only 1 word: Major, Moderate, or Minor."""


# Function to call Groq API
def stream_output(user_prompt):
    try:
        chat_completion = client.chat.completions.create(

        messages=[
            {
                "role": "system",
                "content": system_prompt_ddc
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
        return f"Error with AI API: {str(e)}"


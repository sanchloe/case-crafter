import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DATABRICKS_TOKEN"),
    base_url="https://dbc-1d50e92c-2c27.cloud.databricks.com/serving-endpoints"
)

def get_inference(user_prompt):
    chat_completion = client.chat.completions.create(
        messages=[
        {
            "role": "system",
            "content": "You are an AI assistant"
        },
        {
            "role": "user",
            "content": user_prompt
        }
        ],
            model="databricks-meta-llama-3-1-70b-instruct",
            max_tokens=256
        )

    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content
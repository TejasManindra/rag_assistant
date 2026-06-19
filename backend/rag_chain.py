import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def generate_answer(query, context):

    prompt = f"""
You are an expert document assistant.

Answer ONLY from the provided context.

If multiple sections are relevant,
combine them into a complete answer.

If the answer is not clearly present,
say:
'I could not find that information in the document.'

Context:
{context}

Question:
{query}
"""

    start = time.time()

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print(f"LLM Time: {time.time()-start:.2f}s")

    return response.choices[0].message.content
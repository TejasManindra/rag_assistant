import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def generate_answer(query, context,chat_history=""):

    prompt = f"""
You are a helpful AI assistant.

Answer using ONLY the provided context.

Instructions:
1. Use previous conversation if relevant.
2. Use the document context.
3. If answer is not available, say so.
4. Be concise and accurate.

Rules:
1. Use information from all retrieved chunks.
2. Combine information from multiple chunks.
3. If the answer is partially available, provide the partial answer.
4. Only say "I could not find that information in the document"
   if no relevant information exists in the context.
5. Format answers clearly using bullet points or tables when useful.

Previous Conversation:
{chat_history}

Document Context:
{context}

Current Question:
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
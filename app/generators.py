# generators.py
import asyncio
import httpx
from openai import AsyncOpenAI

from config import AI_KEY
from config import PROXY


client = AsyncOpenAI(api_key=AI_KEY,
                     http_client=httpx.AsyncClient(proxies=PROXY,
                                                   transport=httpx.HTTPTransport(local_address="0.0.0.0")))

async def gpt_text(messages, model, temperature=0.7, max_tokens=None):
    completion = await client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return completion.choices[0].message.content
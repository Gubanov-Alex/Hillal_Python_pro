import json
import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI

import asyncio
import httpx

load_dotenv(dotenv_path="/home/oleksandr/PycharmProjects/Hillal_Python_pro/lesson12/API_for_currency_change_AI_1.0/Backend/API_KEY.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_KEY = os.getenv("API_KEY")

if OPENAI_API_KEY and API_KEY:
    print("Environment variables loaded successfully.")
else:
    print("One or more environment variables are missing.")

aclient = AsyncOpenAI(api_key=OPENAI_API_KEY, project="proj_Sb2TGdRdfjgzLbtNdzkbTEWx")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationService:
    """
    A service for generating various content ideas, technical guides, and fiction.

    This class provides asynchronous methods to generate random article ideas, technical
    guides, and fictional content based on user-provided data. It leverages an
    AI model to generate contextually relevant outputs.

    :ivar aclient: Client to interact with the AI model and handle chat completions.
    :type aclient: object
    """
    async def generate_random_article_idea(self, data):
        """
        Generate random article ideas based on the provided data.
        """
        if isinstance(data, dict):
            prompt = json.dumps(data, ensure_ascii=False)
        elif isinstance(data, str):
            prompt = data
        else:
            raise TypeError("Data must be either a dictionary or a string.")

        if not prompt:
            raise ValueError("The prompt text is empty or missing.")

        await asyncio.sleep(5)

        response = await aclient.chat.completions.create(messages=[
             {
                    "role": "system",
                    "content": "You are a helpful assistant that generates random article ideas."
             },
             {
                    "role": "user",
                    "content": prompt
             }
            ],
            model="gpt-4o-mini")

        return response.choices[0].message.content
        #  return "random idea"

    async def generate_technical_guide(self, data):
        """
        Generate technical guides based on the provided data.
        """

        if isinstance(data, dict):
            prompt = json.dumps(data, ensure_ascii=False)
        elif isinstance(data, str):
            prompt = data
        else:
            raise TypeError("Data must be either a dictionary or a string.")

        if not prompt:
            raise ValueError("The prompt text is empty or missing.")

        await asyncio.sleep(5)

        response = await aclient.chat.completions.create(messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates random technical guides."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
            model="gpt-4o-mini")

        return response.choices[0].message.content
        # return "tech guide"

    async def generate_fiction(self, data):
        """
        Generate fiction based on the provided data.
        """
        if isinstance(data, dict):
            prompt = json.dumps(data, ensure_ascii=False)
        elif isinstance(data, str):
            prompt = data
        else:
            raise TypeError("Data must be either a dictionary or a string.")

        if not prompt:
            raise ValueError("The prompt text is empty or missing.")

        await asyncio.sleep(5)

        response = await aclient.chat.completions.create(messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates random fiction."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
            model="gpt-4o-mini")

        return response.choices[0].message.content
        # return "Generate fiction"


@app.get("/fetch-market")
async def fetch_market():
    """
    User Request:           None
    User Response:          str

    Alphavantage Request:   dict
    Alphavantage Response:  dict
    {'Realtime Currency Exchange Rate': {'1. From_Currency Code': 'UAH',
             '2. From_Currency Name': 'Ukrainian '
                                      'Hryvnia',
             '3. To_Currency Code': 'USD',
             '4. To_Currency Name': 'United States '
                                    'Dollar',
             '5. Exchange Rate': '0.02380000',
             '6. Last Refreshed': '2025-01-06 19:37:43',
             '7. Time Zone': 'UTC',
             '8. Bid Price': '0.02379000',
             '9. Ask Price': '0.02380000'}
    }
    """
    url = (
        "https://www.alphavantage.co/query?"
        "function=CURRENCY_EXCHANGE_RATE&"
        "from_currency=UAH&"
        f"to_currency=USD&apikey={API_KEY}"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    await asyncio.sleep(5)
    return {"rate": rate}

@app.post("/article_idea")
async def generate_article(request: Request):
    data = await request.json()
    if not data:
        raise HTTPException(status_code=400, detail="Question is required")
    return {
        "idea": await GenerationService().generate_random_article_idea(data),
        "technical_guide": await GenerationService().generate_technical_guide(data),
        "fiction": await GenerationService().generate_fiction(data),
    }

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
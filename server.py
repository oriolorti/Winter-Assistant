import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "Winter is running"}

@app.post("/chat")
def chat(req: ChatRequest):
    response = client.responses.create(
        model="gpt-5-mini",
        input=req.message
    )

    return {
        "reply": response.output_text
    }

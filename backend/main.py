import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from fastapi.middleware.cors import CORSMiddleware
import selenium_service
import uvicorn



load_dotenv()
app = FastAPI()

# Allow your frontend origin
origins = [
    "http://localhost:5173",  # your React dev server
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Google Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

class PromptRequest(BaseModel):
    prompt: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World 🚀"}

# SemakMule Endpoint
@app.get("/api/check/phone_number/{number}")
def check_phone_num(number: str):
    try:
        result = selenium_service.check_phone_number(number)
        return {
            "result": result
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/check/bank_number/{number}")
def check_bank_num(bankNum: str):
    return {
        "bank_number": bankNum
    }

@app.get("/api/check/email/{email}")
def check_email(email: str):
    return {
        "email": email
    }

# Phishing Detection Endpoint
@app.post("/api/check/phishing")
def check_phishing(sentence: str):
    return {
        "result": True
    }

@app.post("/api/chat")
async def chat(request: PromptRequest):
    try:
        response = llm.invoke([
            HumanMessage(content=request.prompt)
        ])

        return {
            "input": request.prompt,
            "response": response.content
        }

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # This matches your terminal command but lives inside your code
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
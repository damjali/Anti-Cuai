import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from fastapi.middleware.cors import CORSMiddleware

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

# 1. FIXED: Updated to a currently supported model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

class PromptRequest(BaseModel):
    prompt: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World 🚀"}

# 2. FIXED: Matched path parameters and gave unique function names
@app.get("/api/check/phone_number/{phoneNum}")
def check_phone_number(phoneNum: int):
    return {
        "phone_number": phoneNum
    }

@app.get("/api/check/bank_number/{bankNum}")
def check_bank_number(bankNum: int):
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
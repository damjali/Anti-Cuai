import os
import requests
from fastapi import FastAPI, HTTPException
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

# 1. FIXED: Updated to a currently supported model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# Class Declarations
class PromptRequest(BaseModel):
    prompt: str

class PhishingRequest(BaseModel):
    url: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World 🚀"}

# SemakMule Endpoint
@app.get("/api/check/phone_number/{number}")
def check_phone_num(number: str):
    try:
        result = selenium_service.check_phone_number(number)
        return result
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/check/bank_number/{bankNum}")
def check_bank_num(bankNum: str):
    try:
        result = selenium_service.check_account_no(bankNum)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/check/company_name/{companyName}")
def check_company_name(companyName: str):
    try:
        result = selenium_service.check_company_name(companyName)
        return result
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/check/phishing")
def check_phishing(request: PhishingRequest):
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise HTTPException(status_code=500, detail="Google API Key not configured")

    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    
    payload = {
        "client": {"clientId": "anti-cuai-app", "clientVersion": "1.0.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": request.url}]
        }
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        data = response.json()

        # Case 1: URL is SAFE (No matches found)
        if "matches" not in data:
            return {
                "url": request.url,
                "status": "safe",
                "is_phishing": False,
                "message": "No known threats detected. This link appears safe.",
                "risk_level": "Low",
                "details": []
            }

        # Case 2: URL is MALICIOUS (Matches found)
        matches = data.get("matches", [])
        
        # Extract specific threats to create a custom warning
        threat_types = [m.get("threatType") for m in matches]
        
        # Logic to determine the primary warning message
        if "SOCIAL_ENGINEERING" in threat_types:
            msg = "Warning: This looks like a phishing site designed to steal your credentials!"
            risk = "Critical"
        elif "MALWARE" in threat_types:
            msg = "Danger: This site is known to distribute malicious software."
            risk = "High"
        elif "UNWANTED_SOFTWARE" in threat_types:
            msg = "Caution: This site may try to install tricky or unwanted programs."
            risk = "Medium"
        else:
            msg = "Warning: This site is flagged as potentially harmful."
            risk = "High"

        return {
            "url": request.url,
            "status": "malicious",
            "is_phishing": True,
            "message": msg,
            "risk_level": risk,
            "threat_count": len(matches),
            "details": [
                {
                    "type": m.get("threatType").replace("_", " ").title(),
                    "platform": m.get("platformType").replace("_", " ").title(),
                    "detected_at": m.get("threat", {}).get("url")
                } for m in matches
            ]
        }
        
    except requests.exceptions.RequestException as e:
        # Check if it's a 403 (Permission) or 400 (Bad Request) specifically
        status_code = e.response.status_code if e.response else 500
        return {
            "status": "error",
            "error_code": status_code,
            "message": f"Security check failed: {str(e)}"
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
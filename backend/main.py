from fastapi import FastAPI
import selenium_service
app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World 🚀"}

# SemakMule Endpoint
@app.get("/api/check/phone_number/{number}")
def get_item(phoneNum: int):
    return {
        "phone_number": phoneNum
    }

@app.get("/api/check/bank_number/{number}")
def get_item(bankNum: int):
    return {
        "bank_number": bankNum
    }

@app.get("/api/check/email/{email}")
def get_item(email: str):
    return {
        "email": email
    }

# Phishing Detection Endpoint
@app.post("/api/check/phishing")
def create_item(sentence: str):
    return {
        "result": True
    }
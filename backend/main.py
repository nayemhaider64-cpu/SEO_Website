
import uvicorn
import requests

from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel


# Request body schema
class KeywordRequest(BaseModel):
    keyword: str


# Google suggestions function
def google_suggestions(query: str) -> list[str]:
    url = "https://suggestqueries.google.com/complete/search"

    params = {
        "client": "firefox",
        "q": query,
    }

    result = requests.get(url, params=params, timeout=10)
    result.raise_for_status()

    return result.json()[1]


app = FastAPI()


# 1. TrustedHost Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "myapi.com",
        "*.myapi.com",
        "localhost",
        "127.0.0.1",
    ],
)


# 2. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://myfrontend.com",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def get_recommendations(data: KeywordRequest = Body(...)):
    return google_suggestions(data.keyword)



@app.post("/similar")
def get_data(
    recommendations: list[str] = Depends(get_recommendations),
):
    return {"recommendations": recommendations}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

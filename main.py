from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from data_analysis import analyze_data
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str


@app.post("/analyze")
async def run_query(req: QueryRequest):
    try:
        result = analyze_data(req.query)
        return {"result": result} 
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

from fastapi import FastAPI
from app.agent import run_agent

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI MCP Agent Running"}

@app.get("/query")
def query(q: str):
    response = run_agent(q)
    return {"response": response}
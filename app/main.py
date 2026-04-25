from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import run_agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS (important for frontend UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for POST /chat
class QueryRequest(BaseModel):
    message: str

# Home route
@app.get("/")
def home():
    return {"message": "AI MCP Agent Running 🚀"}

# Old GET endpoint (for testing in browser/Postman)
@app.get("/query")
def query(q: str):
    response = run_agent(q)
    return {"response": response}

# New POST endpoint (used by UI)
@app.post("/chat")
def chat(req: QueryRequest):
    response = run_agent(req.message)
    return {"response": response}
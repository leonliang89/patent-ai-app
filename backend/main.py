from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Header
from fastapi.responses import FileResponse
from auth import verify_token
from agent_runner import run_agent
from patent_analysis import analyze_patents
from db import usage

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FREE_LIMIT = 3

@app.post("/generate")
def generate(data: dict, authorization: str = Header(None)):
    user = verify_token(authorization) if authorization else "guest"

    if user != "admin":
        if usage.get(user, 0) >= FREE_LIMIT:
            return {"error": "Upgrade required"}
        usage[user] = usage.get(user, 0) + 1

    patent = run_agent(data["text"])
    analysis = analyze_patents(data["text"])

    return {
        "patent": patent,
        "analysis": analysis
    }

@app.get("/chart")
def get_chart():
    return FileResponse("output/chart.png")

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from agent_runner import run_agent
from patent_analysis import analyze_patents

app = FastAPI()

# ✅ 解決你卡住的關鍵（CORS）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
def generate(data: dict):
    patent = run_agent(data["text"])
    analysis = analyze_patents(data["text"])
    return {"patent": patent, "analysis": analysis}

@app.get("/chart")
def get_chart():
    return FileResponse("output/chart.png")

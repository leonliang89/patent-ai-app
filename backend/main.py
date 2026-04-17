from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from agent_runner import run_agent
from patent_search import search_patents
from database import get_result
from background import run_large_analysis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/generate')
def generate(data: dict, background_tasks: BackgroundTasks):
    query = data['text']
    cached = get_result(query)
    if cached:
        return {'status': 'done', 'data': cached}
    patents = search_patents(query)[:20]
    background_tasks.add_task(run_large_analysis, query)
    return {'status': 'processing', 'preview': patents}

@app.get('/result/{query}')
def result(query: str):
    data = get_result(query)
    return {'status': 'done', 'data': data}
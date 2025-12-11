# app/main.py
# FastAPI app + endpoints

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any
from app.stores import new_graph, new_run, get_run, get_graph
from app.workflows import NODE_FNS
from app import engine
import asyncio

app = FastAPI(title="Minimal Workflow Engine")

class CreateGraphReq(BaseModel):
    nodes: Dict[str, dict]
    edges: Dict[str, str]
    entry: str

class RunReq(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]

@app.post("/graph/create")
async def create_graph(req: CreateGraphReq):
    for k, meta in req.nodes.items():
        fn_key = meta.get("fn")
        if fn_key not in NODE_FNS:
            raise HTTPException(status_code=400, detail=f"unknown node fn {fn_key}")

        # attach callable to node metadata

        meta["fn"] = NODE_FNS[fn_key]
    gid = new_graph(req.nodes, req.edges, req.entry)
    return {"graph_id": gid}

@app.post("/graph/run")
async def run_graph(req: RunReq, background_tasks: BackgroundTasks):
    graph = get_graph(req.graph_id)
    if not graph:
        raise HTTPException(status_code=404, detail="graph not found")
    rid = new_run(req.graph_id, req.initial_state)

    # start background task to execute run

    loop = asyncio.get_event_loop()
    loop.create_task(engine.execute_run(rid))
    return {"run_id": rid}

@app.get("/graph/state/{run_id}")
async def get_state(run_id: str):
    r = get_run(run_id)
    if not r:
        raise HTTPException(status_code=404, detail="run not found")
    return {"run_id": r.run_id, "status": r.status, "state": r.state, "logs": r.logs, "current_node": r.current_node, "error": r.error}

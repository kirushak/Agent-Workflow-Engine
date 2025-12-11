# app/stores.py
# simple in-memory stores for graphs & runs

from typing import Dict, Any
import uuid
from dataclasses import dataclass, field

@dataclass
class Graph:
    graph_id: str
    nodes: Dict[str, dict]  # metadata for nodes (name etc.)
    edges: Dict[str, str]   # simple mapping: node -> next node or conditional mapping
    entry: str

@dataclass
class Run:
    run_id: str
    graph_id: str
    state: Dict[str, Any] = field(default_factory=dict)
    logs: list = field(default_factory=list)
    status: str = "running"  # running | finished | error
    current_node: str | None = None
    error: str | None = None

GRAPHS: Dict[str, Graph] = {}
RUNS: Dict[str, Run] = {}

def new_graph(nodes: Dict[str, dict], edges: Dict[str, str], entry: str) -> str:
    gid = str(uuid.uuid4())
    GRAPHS[gid] = Graph(graph_id=gid, nodes=nodes, edges=edges, entry=entry)
    return gid

def get_graph(gid: str) -> Graph | None:
    return GRAPHS.get(gid)

def new_run(graph_id: str, initial_state: Dict) -> str:
    rid = str(uuid.uuid4())
    RUNS[rid] = Run(run_id=rid, graph_id=graph_id, state=initial_state.copy())
    return rid

def get_run(rid: str) -> Run | None:
    return RUNS.get(rid)

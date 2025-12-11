# app/engine.py
# Graph engine

import asyncio
from typing import Dict, Any, Callable
from app.stores import get_graph, get_run
from app.tools import TOOLS



async def run_node(node_fn: Callable, run_id: str, state: Dict[str, Any], extras: Dict) -> Dict:
    # ensure node_fn can be awaited
    result = node_fn(state, TOOLS, extras)
    if asyncio.iscoroutine(result):
        result = await result
    return result

async def execute_run(run_id: str):
    run = get_run(run_id)
    if run is None:
        return
    graph = get_graph(run.graph_id)
    if graph is None:
        run.status = "error"
        run.error = "graph_not_found"
        return

    current = graph.entry
    loop_counter = 0
    try:
        while current:
            run.current_node = current
            run.logs.append(f"START {current}")
            node_meta = graph.nodes.get(current)
            node_fn = node_meta.get("fn")
            extras = {"run_id": run_id, "loop_counter": loop_counter}
            out = await run_node(node_fn, run_id, run.state, extras)
            # out may update state, specify next
            if out is None:
                run.logs.append(f"NODE {current} returned None -> stop")
                break
            run.state.update(out.get("state", {}))
            msg = out.get("log")
            if msg:
                run.logs.append(f"{current}: {msg}")
            next_node = out.get("next")
            # fallback to static edges
            if next_node is None:
                next_node = graph.edges.get(current)
            run.logs.append(f"END {current} -> next: {next_node}")
            # detect runaway loops
            loop_counter += 1
            if loop_counter > 1000:
                run.status = "error"
                run.error = "loop_limit_exceeded"
                run.logs.append("Loop limit exceeded")
                return
            current = next_node
        run.status = "finished"
        run.current_node = None
        run.logs.append("RUN FINISHED")
    except Exception as e:
        run.status = "error"
        run.error = str(e)
        run.logs.append(f"ERROR: {e}")

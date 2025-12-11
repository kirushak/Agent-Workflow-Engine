
import asyncio
from typing import Dict, Any
from app.tools import TOOLS
def extract_functions(code: str) -> Dict[str, Any]:
    # naive split by "def " to find functions
    parts = code.split("\n")
    functions = []
    current = []
    in_fn = False
    for line in parts:
        if line.strip().startswith("def "):
            if in_fn:
                functions.append("\n".join(current))
            current = [line]
            in_fn = True
        else:
            if in_fn:
                current.append(line)
    if in_fn and current:
        functions.append("\n".join(current))
    return {"functions": functions}

async def node_extract(state: Dict[str, Any], tools: Dict, extras: Dict):
    code = state.get("code", "")
    state_updates = extract_functions(code)
    return {"state": state_updates, "next": "check_complexity", "log": f"extracted {len(state_updates.get('functions', []))} functions"}

async def node_check_complexity(state: Dict[str, Any], tools: Dict, extras: Dict):
    funcs = state.get("functions", [])
    complexities = []
    for f in funcs:
        c = tools["complexity_estimate"](f)
        complexities.append(c["complexity"])
    avg = sum(complexities)/len(complexities) if complexities else 0
    state_updates = {"complexities": complexities, "avg_complexity": avg}
    return {"state": state_updates, "next": "detect_issues", "log": f"avg_complexity={avg}"}

async def node_detect_issues(state: Dict[str, Any], tools: Dict, extras: Dict):
    code = state.get("code", "")
    res = tools["detect_smells"](code)
    issues = res.get("issues", 0)
    state_updates = {"issues": issues}
    return {"state": state_updates, "next": "suggest_improvements", "log": f"issues={issues}"}

async def node_suggest_improvements(state: Dict[str, Any], tools: Dict, extras: Dict):
    suggestions = []
    if state.get("avg_complexity", 0) > 10:
        suggestions.append("Consider splitting large functions.")
    if state.get("issues", 0) > 0:
        suggestions.append("Remove TODOs and prints; address basic smells.")

    # quality score (higher better); heuristic

    score = max(0, 100 - int(state.get("avg_complexity", 0) * 3) - state.get("issues", 0) * 5)
    state_updates = {"suggestions": suggestions, "quality_score": score}
    return {"state": state_updates, "next": "maybe_loop", "log": f"quality_score={score}"}

async def node_maybe_loop(state: Dict[str, Any], tools: Dict, extras: Dict):
    threshold = state.get("threshold", 80)
    score = state.get("quality_score", 0)
    if score < threshold:

        # pretend to "apply improvements" and re-check: mutate code slightly
        # in real world you'd apply patches; here we simulate improvement

        state_updates = {"code": state.get("code", "") + "\n# applied suggestion", "loop_count": state.get("loop_count", 0) + 1}

        # Jump back to check_complexity to re-evaluate

        return {"state": state_updates, "next": "check_complexity", "log": f"looping, score {score} < {threshold}"}
    else:
        return {"state": {}, "next": None, "log": f"stopping, score {score} >= {threshold}"}


NODE_FNS = {
    "extract": node_extract,
    "check_complexity": node_check_complexity,
    "detect_issues": node_detect_issues,
    "suggest_improvements": node_suggest_improvements,
    "maybe_loop": node_maybe_loop,
}

# app/tools.py
# tool registry + sample tools

from typing import Dict, Any

TOOLS: Dict[str, callable] = {}

def register_tool(name: str):
    def decorator(fn):
        TOOLS[name] = fn
        return fn
    return decorator

@register_tool("detect_smells")
def detect_smells(code: str) -> Dict[str, Any]:
    # naive rule-based smell detector
    issues = 0
    if "TODO" in code:
        issues += 1
    if "print(" in code:
        issues += 1
    if len(code.splitlines()) > 200:
        issues += 1
    return {"issues": issues}

@register_tool("complexity_estimate")
def complexity_estimate(fn_source: str) -> Dict[str, Any]:
    # very naive: count conditionals/loops as complexity proxies
    score = 1
    for token in ("for ", "while ", "if ", "elif ", "try:", "except"):
        score += fn_source.count(token)
    return {"complexity": score}

#!/bin/bash

echo "📝 Generating README.md ..."

cat << 'EOF' > README.md
# 🚀 AI Workflow Engine  
### _A Minimal LLM-Inspired Workflow / Agent Graph Framework built with FastAPI_

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" />
  <img src="https://img.shields.io/badge/FastAPI-Workflow%20Engine-green" />
  <img src="https://img.shields.io/badge/Async-Enabled-purple" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
</p>

---

## 🌟 Overview

**AI Workflow Engine** is a lightweight, modular, and extensible **graph-based execution framework** inspired by LLM agent orchestration systems.  
It lets you define **nodes**, connect them via **edges**, and execute them with shared **state**, tools, branching, loops, and async processing.

A fully working sample:  
➡️ **Code Review Mini-Agent** (extracts functions, analyzes complexity, detects issues, loops until quality threshold)

---

## ✨ Key Features

- 🧩 **Node-Based Workflows**
- 🔗 **Graph Execution Engine**
- 🧠 **Shared State**
- 🔁 **Looping & Conditional Branching**
- ⚡ **Async Execution**
- 🧰 **Tool Registry**
- 📡 **FastAPI Endpoints**
- 📜 **Execution Logs & Run State**

---

# 📂 Project Structure

\`\`\`
aieng-workflow/
├── app/
│   ├── main.py
│   ├── engine.py
│   ├── tools.py
│   ├── workflows.py
│   ├── stores.py
├── requirements.txt
└── README.md
\`\`\`

---

# ⚙️ Installation

\`\`\`bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
\`\`\`

---

# 🧪 Using the Sample Workflow

## 1️⃣ Create Graph  
POST → `/graph/create`

\`\`\`json
{
  "nodes": {
    "extract": {"fn": "extract"},
    "check_complexity": {"fn": "check_complexity"},
    "detect_issues": {"fn": "detect_issues"},
    "suggest_improvements": {"fn": "suggest_improvements"},
    "maybe_loop": {"fn": "maybe_loop"}
  },
  "edges": {
    "extract": "check_complexity",
    "check_complexity": "detect_issues",
    "detect_issues": "suggest_improvements",
    "suggest_improvements": "maybe_loop"
  },
  "entry": "extract"
}
\`\`\`

---

## 2️⃣ Run Workflow  
POST → `/graph/run`

\`\`\`json
{
  "graph_id": "<graph-id>",
  "initial_state": {
    "code": "def foo():\n    print(1)\n",
    "threshold": 80
  }
}
\`\`\`

---

## 3️⃣ Check Run Status  
GET → `/graph/state/<run_id>`

Example:

\`\`\`json
{
  "status": "finished",
  "state": {
    "avg_complexity": 3,
    "issues": 1,
    "quality_score": 85
  }
}
\`\`\`

---

# 🤖 Code Review Mini-Agent Workflow

✔ Function Extraction  
✔ Complexity Analysis  
✔ Code Smell Detection  
✔ Suggestions Generation  
✔ Loop until threshold achieved  

---

# 🧱 Architecture

### Node Function Format
\`\`\`python
async def node_fn(state, tools, extras):
    return {
        "state": {...},
        "next": "node_key",
        "log": "message"
    }
\`\`\`

### Execution Process
1. Start at entry node  
2. Execute node  
3. Update state  
4. Route to next node  
5. Stop when next = None  

---

# 🔮 Future Enhancements

- DB storage (SQLite/Postgres)  
- WebSocket streaming logs  
- Conditional edge DSL  
- LLM-powered nodes  
- Dashboard visualization  

---



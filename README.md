#!/bin/bash

cat << 'EOF' > README.md
# 🎯 **AI Workflow Engine**
### _Tiny. Modular. Async. Agentic._

<p align="center">
  <img src="https://img.shields.io/badge/Build-Minimal-black?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-0ea5e9?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Agentic-Workflows-purple?style=for-the-badge" />
</p>

---

## 🌟 What It Is  
A super-light **graph-based workflow engine** for AI/LLM pipelines.  
Think: *nodes → edges → shared state → async execution*.

---

## ⚡ Highlights  
- ⚙️ Node-driven graph execution  
- 🔁 Conditional edges + loops  
- 📦 Shared mutable state  
- ⚡ Async support  
- 🧰 Tool registry  
- 🌐 FastAPI routes  

---

## 🧩 Architecture
\`\`\`
app/
 ├── engine.py
 ├── main.py
 ├── tools.py
 ├── workflows.py
 └── stores.py
\`\`\`

---

## 🚀 Quick Start
\`\`\`bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
\`\`\`

---

## 🛰 API
- POST /graph/create  
- POST /graph/run  
- GET /graph/state/{run_id}  

---

## 🤖 Example Workflow
Code Review Mini-Agent.

---






# FinWise

### Your Money. Your Decisions. Powered by AI.

FinWise is an agentic AI-powered expense management platform designed to help students and young individuals understand their spending, identify financial patterns and make informed budgeting decisions.

Developed during the **B/STACK RAG-A-THON 2026**.

## The Problem

Managing everyday expenses can be challenging, especially for students living independently. Traditional expense trackers record transactions but often lack intelligent analysis and actionable insights.

FinWise bridges this gap by combining expense tracking with an AI agent capable of executing financial analysis tools.

## Key Features

- **Expense Tracking** — Record and categorize daily expenses.
- **Smart Dashboard** — Visualize spending patterns and category-wise expenses.
- **Agentic AI Assistant** — Analyze recorded expenses through natural-language queries.
- **Subscription Detection** — Identify recurring subscription payments.
- **Anomaly Detection** — Identify unusual spending.
- **RAG Knowledge Retrieval** — Retrieve relevant information from a financial knowledge base.
- **Budget Planning** — Generate budgeting proposals.
- **Human-in-the-Loop** — Require explicit approval for budget proposals.
- **Execution Transparency** — Inspect tool execution, recovery and validation traces.

## What Makes FinWise Agentic?

Unlike a conventional chatbot, FinWise uses an AI agent that can select and execute specialized tools, retrieve financial knowledge, validate tool results and recover missing tool executions.

## System Architecture

```text
User
  |
Streamlit Frontend
  |
Intent Router
  |
LangGraph AI Agent
  |
Qwen Language Model
  |
  +-- Transaction Analysis
  +-- Subscription Detection
  +-- Recurring Payment Detection
  +-- Anomaly Detection
  +-- Budget Planning
  +-- Financial Knowledge Retrieval
  |
Result Validation & Tool Recovery
  |
Human Approval (when required)
  |
Financial Insights
```

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| AI Model | Qwen 2.5 |
| Agent Framework | LangGraph |
| Tool Integration | LangChain |
| Local Inference | Ollama |
| Cloud Inference | llama.cpp |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Knowledge Retrieval | Custom RAG pipeline |
| Version Control | Git & GitHub |

## Available AI Tools

| Tool | Purpose |
|---|---|
| `analyze_transactions` | Analyze spending and transaction categories |
| `detect_subscriptions` | Identify recurring subscriptions |
| `detect_recurring_payments` | Identify recurring expenses |
| `identify_unusual_expenses` | Detect unusual spending |
| `create_budget_plan` | Generate budget proposals |
| `calculate_remaining_balance` | Calculate balances from supplied financial information |
| `search_financial_knowledge` | Retrieve relevant financial knowledge |

## Installation

Clone the repository:

```bash
git clone https://github.com/piyushguptaa2008/FinWise.git
cd FinWise
```

Create a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

For local Ollama inference, install Ollama and download the model:

```bash
ollama pull qwen2.5:7b
```

Launch the application:

```bash
python -m streamlit run frontend/app.py
```

## Example AI Queries

- Which category costs me the most?
- Analyze my transactions.
- Show my recurring expenses.
- Identify my unusual expenses.
- Explain the 50/30/20 budgeting rule.
- Analyze my transactions and detect my subscriptions.

## Responsible AI

FinWise is designed with safeguards including tool-result validation, execution transparency, missing-information handling and explicit human approval for budget proposals.

FinWise provides educational financial insights and does not execute banking transactions or investments.

## Current Limitations

- AI inference may take longer on CPU-based hosting.
- Natural-language intent routing does not cover every possible query.
- Financial knowledge retrieval is limited to the curated knowledge base.
- This application is a hackathon prototype, not a production financial service.

## Future Scope

- Secure account-based persistent storage.
- Bank statement import.
- Personalized spending recommendations.
- Improved financial knowledge retrieval.
- Multilingual financial assistance.
- Mobile application.

## Team

| Member | Contribution |
|---|---|
| Piyush Gupta: Team Lead, Agentic AI, RAG and Integration |
| Niraj Manoj: Chauhan Backend Development and Integration |
| Wahhab Sheikh: Frontend Development and UI/UX |
| Alwaz Hussain: Dataset Development and Testing |
| Omkar Gunge Presentation and Documentation |

## Live Demo

Deployment link will be added after final deployment.

## Repository

https://github.com/piyushguptaa2008/FinWise

---

**FinWise — Make your money make sense.**
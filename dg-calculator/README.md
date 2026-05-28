# DG Size Calculator

A full-stack agentic AI app that calculates the optimal solar panel system size for any location.

## Tech Stack
- **Backend** — FastAPI + MCP (one port, one process)
- **AI Agent** — Groq (Llama 3.1) with function calling
- **Frontend** — React + Vite
- **Database** — MongoDB Atlas

## Project Structure
```
dg-calculator/
├── backend/
│   ├── app/
│   │   ├── domain.py      # Core calculation logic
│   │   ├── main.py        # FastAPI + MCP server
│   │   ├── agent.py       # AI agent (Groq)
│   │   └── database.py    # MongoDB connection
│   ├── .env               # API keys (not committed)
│   └── requirements.txt
└── frontend/              # React app
```

## Setup

### 1. Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create `backend/.env`:
```
GROQ_API_KEY=your_groq_key
MONGO_URI=your_mongodb_uri
DB_NAME=dg_calculator
```

Start the backend:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

## Usage
- **Calculator tab** — enter energy details manually, get instant results
- **AI Assistant tab** — describe your needs in plain English, AI calculates for you

Example: *"I need solar panels for a house that uses 30 kWh a day in Mumbai"*

## API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/calculate` | POST | Calculate DG size |
| `/agent` | POST | AI natural language query |
| `/history` | GET | Recent calculations |
| `/health` | GET | Server status |
| `/mcp` | POST | MCP interface for AI agents |
```

Then save your requirements file:

```powershell
cd backend
.venv\Scripts\activate
pip freeze > requirements.txt
```


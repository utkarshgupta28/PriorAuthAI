# PriorAuth AI

Clinical prior authorization workflow with a staged 3-agent pipeline.

## Stack

- Frontend: React + Vite + Tailwind CSS
- Backend: FastAPI + SQLite
- Agents: CrewAI orchestration with OpenRouter-compatible models

## Active Workflow

1. Policy & Requirements Engine
2. Case Intelligence Engine
3. Submission & Tracker

The pipeline is staged:

1. Run clinical review first
2. Doctor reviews and edits the application
3. Submit to insurance
4. Submission & Tracker starts only after submission

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# add OPENROUTER_API_KEY if using live AI mode
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/cases` | List all cases |
| POST | `/api/cases` | Create a case |
| GET | `/api/cases/{id}` | Get case, outputs, provider context, and history |
| POST | `/api/cases/{id}/run` | Run agents 1-2 clinical review |
| POST | `/api/cases/{id}/submit` | Submit edited doctor-approved application and run agent 3 |
| GET | `/api/cases/{id}/outputs` | Get agent outputs |
| GET | `/api/cases/{id}/insights` | Get case insights |
| POST | `/api/cases/{id}/approve` | Simulate approval |
| POST | `/api/cases/{id}/deny` | Simulate denial |
| GET | `/api/metrics` | Aggregate metrics |

## Environment

```env
OPENROUTER_API_KEY=your_key_here
```

## Fallback Mode

Fallback mode is intentionally kept in place. It provides offline behavior when no live model key is available or a model call fails. For a production healthcare workflow, that is safer than depending on a free-tier API key with unstable quotas, rate limits, or changing availability.

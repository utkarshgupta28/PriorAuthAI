# PriorAuth AI

PriorAuth AI is a healthcare prior authorization workflow app with a staged 3-step review and submission flow.

## Stack

- Frontend: React + Vite + Tailwind CSS
- Backend: FastAPI + SQLite
- AI orchestration: direct provider API calls plus deterministic fallback logic

## Current Workflow

1. Policy Review
2. Clinical Review
3. Submission Tracking

The workflow is intentionally staged:

1. Run review first
2. Review and edit the application draft
3. Confirm doctor approval
4. Submit to insurance
5. Start submission tracking and follow-up

## Key Features

- Case intake and case list dashboard
- Policy and clinical review outputs
- Approval likelihood, case strength, and evidence-based insights
- Editable submission draft before submission
- Doctor approval gate before tracking starts
- Optional supporting-document upload for demo use
- Denial simulation, appeal guidance, and follow-up timeline
- Fallback mode when live AI is unavailable

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Railway Deployment

Deploy this repo to Railway as two services:

1. `backend` service
2. `frontend` service

### Backend Service

- Root directory: `backend`
- Build command:

```bash
pip install -r requirements.txt
```

- Start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

- Required environment variables:

```env
API_KEY=your_provider_key_here
API_BASE_URL=https://api.mistral.ai/v1
MODEL=mistral-small-latest
CORS_ORIGINS=https://your-frontend-service.up.railway.app
```

### Frontend Service

- Root directory: `frontend`
- Build command:

```bash
npm install && npm run build
```

- Start command:

```bash
npm run start
```

- Required environment variables:

```env
VITE_API_BASE_URL=https://your-backend-service.up.railway.app/api
```

### Notes

- Set `CORS_ORIGINS` on the backend to the public Railway URL of the frontend service.
- Set `VITE_API_BASE_URL` on the frontend to the public Railway URL of the backend service.
- SQLite will work for a demo deployment, but Railway volumes or a hosted database are better if you need persistent production data.

## Environment

The backend uses a single provider key and a single model configuration.

```env
API_KEY=your_provider_key_here
API_BASE_URL=https://api.mistral.ai/v1
MODEL=mistral-small-latest
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

If `API_KEY` is blank, the app runs in deterministic fallback mode.

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/cases` | List all cases |
| GET | `/api/demo-presets` | Get demo intake presets |
| POST | `/api/cases` | Create a case |
| DELETE | `/api/cases/{id}` | Delete a case |
| GET | `/api/cases/{id}` | Get case, outputs, provider context, and history |
| POST | `/api/cases/{id}/run` | Run policy review and clinical review |
| POST | `/api/cases/{id}/submit` | Submit doctor-approved application and start tracking |
| GET | `/api/cases/{id}/outputs` | Get agent outputs |
| GET | `/api/cases/{id}/insights` | Get case insights |
| POST | `/api/cases/{id}/approve` | Simulate approval |
| POST | `/api/cases/{id}/deny` | Simulate denial |
| GET | `/api/metrics` | Get dashboard metrics |

## Notes

- The current backend is not using CrewAI.
- The current project is not using hybrid multi-provider orchestration.
- The active supported live path is a direct provider API call using the values in `backend/.env`.
- Fallback mode is kept intentionally so the demo still works if live AI is unavailable.

# Universal Hackathon Base System

Tech stack: FastAPI (Python 3.11), React (Vite + Tailwind), PostgreSQL, Redis, HuggingFace + IsolationForest, JWT Auth, SMTP email, Docker Compose.

## Quickstart (Docker)
1. Copy envs:
   - `cp backend/.env.example backend/.env`
   - `cp frontend/.env.example frontend/.env`
2. Start services:
   - `docker compose up --build`
3. Open frontend: http://localhost:5173
4. API docs: http://localhost:8000/docs

Default DB URL and Redis are in compose; adjust via env if needed. On first run, models auto-create and mock scheduler is registered.

## Local Dev (without Docker)
- Backend: Python 3.11+
  - `cd backend && python -m venv .venv && source .venv/bin/activate`
  - `pip install -r requirements.txt`
  - `cp .env.example .env`
  - `uvicorn app.main:app --reload`
- Frontend:
  - `cd frontend && npm i`
  - `cp .env.example .env`
  - `npm run dev`

## Features
- JWT auth (roles: admin, user), API key auth support
- Data ingestion templates + mock generator + APScheduler periodic jobs
- Realtime via WebSocket + Redis pub/sub
- AI analytics: sentiment (HuggingFace), anomaly (IsolationForest), scoring
- Dashboard with charts, tables, notifications
- SMTP email + in-app notifications
- Plugin system: add new challenge tracks in minutes

## Plugin System
- Backend `app/plugins/<plugin>`:
  - `plugin_config.json` with metadata
  - `backend.py` exporting `router` and optional `init_plugin(app)`
- Frontend `src/plugins/<plugin>/frontend.tsx`
- Backend auto-loads enabled plugins. Frontend dynamically imports UI.

### Create a Plugin
1. Backend: copy `app/plugins/customer_onboarding` and edit the two files
2. Frontend: copy `src/plugins/customer_onboarding/frontend.tsx`
3. Enable in `plugin_config.json` (`"enabled": true`)
4. Restart backend and frontend

## Testing
- `cd backend && pytest -q`

## Environment
- See `backend/.env.example` and `frontend/.env.example`

## Notes
- The first sentiment run downloads a model; keep internet access.
- For HTTPS, place a reverse proxy or terminate TLS at an ingress.
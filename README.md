# Control Board — Full-Stack Task & Project Management Platform

A full-stack project/task management tool built to demonstrate end-to-end software
engineering: REST API design, OOP + repository pattern, a React dashboard with live
analytics, automated testing, and a Dockerized CI/CD pipeline.

## Stack

| Layer      | Tech |
|------------|------|
| Backend    | Python, Flask, SQLAlchemy (repository pattern), REST API |
| Frontend   | React 18, Vite, Tailwind CSS, Recharts |
| Database   | SQLite (dev/prod file-based; swappable to Postgres via `DATABASE_URL`) |
| Testing    | Pytest (25 API tests, all passing) |
| DevOps     | Docker, Docker Compose, GitHub Actions CI/CD |
| Analytics  | Custom `/api/stats` endpoints — completion rate, avg close time, weekly task trend, priority breakdown |

## Project structure

```
task-management-platform/
├── backend/
│   ├── app/
│   │   ├── models/          # Project, Task, Comment (SQLAlchemy ORM)
│   │   ├── routes/          # Flask blueprints: projects, tasks, comments, stats
│   │   ├── repository.py    # Repository pattern — routes never touch db.session directly
│   │   ├── config.py        # Dev / Test / Prod config classes
│   │   └── __init__.py      # App factory
│   ├── tests/                # 25 pytest tests across projects, tasks, comments, stats
│   ├── requirements.txt
│   ├── Dockerfile
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── pages/            # Dashboard, Projects, ProjectDetail, TaskDetail
│   │   ├── components/       # Navbar, StatCard, Badges
│   │   └── api/client.js     # Central fetch wrapper
│   ├── Dockerfile            # Multi-stage build served via nginx
│   └── package.json
├── docker-compose.yml
└── .github/workflows/ci.yml  # Runs tests + builds both Docker images on every push
```

## Run locally (without Docker)

**Backend:**
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py          # runs on http://localhost:5000
```

**Frontend** (separate terminal):
```bash
cd frontend
npm install
cp .env.example .env    # VITE_API_URL=http://localhost:5000
npm run dev              # runs on http://localhost:5173
```

## Run with Docker Compose (recommended — matches production setup)

```bash
docker-compose up --build
```
- Backend: http://localhost:5000
- Frontend: http://localhost:4173

## Run the tests

```bash
cd backend
pytest -v          # 25 tests: CRUD, validation, cascading deletes, stats logic
```

## API overview

| Method | Endpoint | Description |
|--------|----------|--------------|
| GET/POST | `/api/projects` | List / create projects |
| GET/PUT/DELETE | `/api/projects/<id>` | Get / update / delete a project |
| GET/POST | `/api/tasks` | List (filter by `project_id` or `status`) / create tasks |
| GET/PUT/DELETE | `/api/tasks/<id>` | Get / update / delete a task |
| GET/POST | `/api/tasks/<id>/comments` | List / add comments on a task |
| GET | `/api/stats/overview` | KPI summary: totals, completion rate, avg close time |
| GET | `/api/stats/tasks-per-week` | Weekly task creation trend |
| GET | `/api/stats/by-priority` | Task count grouped by priority |
| GET | `/api/health` | Health check |

## Deployment (Render — free tier, recommended)

### 1. Push to GitHub
```bash
cd task-management-platform
git init
git add .
git commit -m "Initial commit: full-stack task management platform"
git branch -M main
git remote add origin https://github.com/<your-username>/task-management-platform.git
git push -u origin main
```

### 2. Deploy the backend on Render
1. Go to [render.com](https://render.com) → **New +** → **Web Service**
2. Connect your GitHub repo, set **Root Directory** to `backend`
3. Render auto-detects the `Dockerfile` — leave build/start commands blank
4. Add environment variable: `SECRET_KEY` = (generate a random string)
5. Deploy. Note the live URL, e.g. `https://control-board-api.onrender.com`

### 3. Deploy the frontend on Render (or Vercel/Netlify)
**Render (Static Site):**
1. **New +** → **Static Site**, Root Directory = `frontend`
2. Build command: `npm install && npm run build`
3. Publish directory: `dist`
4. Environment variable: `VITE_API_URL` = your backend URL from step 2
5. Deploy. You'll get e.g. `https://control-board.onrender.com`

**Vercel (alternative, often faster):**
```bash
cd frontend
npm i -g vercel
vercel --prod
# When prompted, set VITE_API_URL env var to your backend URL
```

### 4. Update CORS if needed
The backend already has `flask-cors` enabled for all origins by default — fine for a
portfolio project. For production hardening, restrict `CORS(app)` in `backend/app/__init__.py`
to your specific frontend domain.

## What this project demonstrates (for recruiters / JD-matching)

- **Backend engineering**: REST API design, OOP domain modeling, repository pattern for
  separation of concerns, input validation, proper HTTP status codes
- **Frontend engineering**: component architecture, client-side routing, live API
  integration, data visualization
- **Testing discipline**: 25 automated tests covering happy paths, validation errors,
  and cascading relationships
- **DevOps**: containerization, multi-service orchestration, CI pipeline that gates
  merges on passing tests and successful builds
- **Data literacy**: purpose-built analytics endpoints (completion rate, cycle time,
  trend-over-time) — not just CRUD

## Customizing per job description

This codebase is intentionally modular so you can tailor it to a specific JD before applying:
- **JD wants more DevOps?** Add a CD step to `.github/workflows/ci.yml` that deploys to
  Render/Railway automatically on merge to `main` (Render supports deploy hooks).
- **JD wants more testing?** Add Playwright/Selenium UI tests in a new `frontend/tests/`
  folder hitting the deployed URL.
- **JD wants more backend depth?** Add JWT auth (`flask-jwt-extended`), role-based
  permissions on projects, or pagination on list endpoints.
- **JD wants cloud experience?** Swap SQLite for Postgres (`DATABASE_URL` env var is
  already wired up in `config.py`) and deploy on AWS/Azure instead of Render.

## License
MIT — free to use as a personal portfolio project.

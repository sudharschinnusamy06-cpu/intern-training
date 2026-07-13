# Employee/Project Management System API — Capstone (Day 29-30)

## Overview
A multi-user REST API where authenticated users can create projects, add members,
and (Day 30) manage tasks inside those projects. Role-based access, JWT auth,
Redis caching, full Docker Compose stack.

## Tech Stack
- FastAPI + Uvicorn
- PostgreSQL (via SQLModel / async SQLAlchemy)
- Redis (caching)
- JWT auth (python-jose) + bcrypt password hashing
- Docker + docker-compose (app + db + redis)
- pytest (Day 30)
- GitHub Actions CI/CD (Day 30)
- AWS EC2 deployment (Day 30)

## Database Schema
- `users` — id, username, email, hashed_password, role, created_at
- `projects` — id, name, description, owner_id (FK -> users.id), created_at
- `project_members` — id, project_id (FK), user_id (FK) — link table
- `tasks` — id, title, description, status, project_id (FK), assigned_to (FK), created_at (Day 30)

## Setup — Run Locally

1. Clone the repo and go to this folder:
cd day29-30-capstone

2. Copy env template and fill real values:
copy .env.example .env

3. Build and start the full stack (app + Postgres + Redis):
docker-compose up --build

4. App runs at: `http://localhost:8000`
   Swagger docs at: `http://localhost:8000/docs`

5. To stop:
docker-compose down

## API Endpoints (Day 29)

| Method | Path | Description |
|---|---|---|
| POST | /auth/register | Create a new user |
| POST | /auth/login | Login, get JWT access token |
| POST | /projects/ | Create a project (creator auto-added as member) |
| GET | /projects/ | List projects the logged-in user is a member of |
| GET | /projects/{project_id} | Get project details (must be a member) |
| POST | /projects/{project_id}/members | Add a member (owner only) |

## Testing via Swagger UI

1. Go to `/auth/register`, create a test user (username, email, password)
2. Go to `/auth/login`, log in with same credentials
3. Click green **Authorize** button (top right), enter username/password, click Authorize
4. Now try `/projects/` POST with:
```json
   { "name": "Test Project", "description": "Testing" }
```
5. Response should return `200` with the new project's id and owner_id

## Issues Faced & Fixes (Day 29)

- **Port 5432 conflict**: local Windows PostgreSQL already used port 5432, so
  Docker Postgres was mapped to host port `5433` instead (`"5433:5432"` in
  docker-compose.yml), while staying `5432` internally between containers.
- **JWT "sub" type mismatch**: JWT `sub` claim must be a string (`str(user.id)`
  when creating the token), but `session.get()` needs an integer primary key —
  fixed by converting back with `int(user_id)` in `dependencies.py`.

## Commands Used

```powershell
git checkout -b day29-capstone-setup
docker-compose up --build
docker-compose logs app --tail=50
docker-compose down
```

## Status
Day 29 — core auth + project CRUD + membership working, tested via Swagger.
Remaining: tasks router (Day 30), pytest suite, CI/CD, AWS deployment.
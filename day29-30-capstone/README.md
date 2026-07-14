# Employee/Project Management System API — Capstone (Day 29-30)

## Overview
A multi-user REST API where authenticated users manage projects and tasks
inside them, with role-based membership, JWT auth, Redis caching, async
endpoints, pagination/filtering, full Docker Compose stack, CI/CD, and AWS
EC2 deployment.

## Tech Stack
- FastAPI + Uvicorn
- PostgreSQL (SQLModel / async SQLAlchemy)
- Redis (caching)
- JWT auth (python-jose) + bcrypt password hashing
- Docker + docker-compose (app + db + redis)
- pytest
- GitHub Actions CI/CD
- AWS EC2 deployment

## Database Schema
- `users` — id, username, email, hashed_password, role, created_at
- `projects` — id, name, description, owner_id (FK → users.id), created_at
- `project_members` — id, project_id (FK), user_id (FK), unique(project_id, user_id)
- `tasks` — id, title, description, status, project_id (FK), assigned_to (FK), created_at

## API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | /auth/register | Create a new user |
| POST | /auth/login | Login, get JWT access token |
| POST | /projects/ | Create a project (creator auto-added as member) |
| GET | /projects/ | List projects the logged-in user is a member of |
| GET | /projects/{project_id} | Get project details (must be a member) |
| POST | /projects/{project_id}/members | Add a member (owner only) |
| POST | /projects/{project_id}/tasks/ | Create a task |
| GET | /projects/{project_id}/tasks/ | List tasks — pagination + status filter, Redis cached |
| PUT | /projects/{project_id}/tasks/{task_id} | Update a task |
| DELETE | /projects/{project_id}/tasks/{task_id} | Delete a task |

## Setup — Run Locally

```powershell
cd day29-30-capstone
copy .env.example .env
docker-compose up --build
```
- App: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- Stop: `docker-compose down`

## Testing via Swagger UI

1. `/auth/register` → create a test user (username, email, password)
2. `/auth/login` → log in with same credentials
3. Click **Authorize** (top right) → enter username/password → Authorize
4. `/projects/` POST:
```json
   { "name": "Test Project", "description": "Testing" }
```
5. `/projects/{project_id}/tasks/` POST:
```json
   { "title": "Setup database schema", "description": "Design tables" }
```
6. All should return `200`

## Running Tests

```powershell
docker-compose exec app pytest -v
```
Currently: **11/11 passing** (auth, projects, tasks — unit + integration).

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on every push/PR to `main`:
installs dependencies, runs pytest, builds the Docker image. Verified passing.

## AWS Deployment

Deployed to an existing EC2 instance (Ubuntu, t3.micro, ap-southeast-2).
Full docker-compose stack (app + Postgres + Redis) runs directly on EC2 —
no separate RDS used (brief allows EC2 alone; RDS/S3 optional).

**Live URL (only while instance is running):** `http://<EC2-public-ip>:8000/docs`

**Security group inbound rules:** SSH (22), Custom TCP (8000 — app), HTTP (80), HTTPS (443)

### Restart & Redeploy Steps (after stopping the instance)

Since the instance has no Elastic IP, it gets a **new public IP** every restart.

1. AWS Console → EC2 → Instances → `task-api-server` → Instance state → Start.
   Wait for "Running," note the new Public IPv4 address.
2. SSH in:
```powershell
   cd "C:\Users\Sudharshini\Downloads"
   ssh -i "task-api-key.pem" ubuntu@
```
3. Pull latest code:
```bash
   cd intern-training
   git checkout day29-capstone-setup
   git pull origin day29-capstone-setup
   cd day29-30-capstone
```
4. Recreate `.env` (not committed to Git):
```bash
   nano .env
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/capstonedb
REDIS_URL=redis://redis:6379/0
JWT_SECRET_KEY=capstone-production-secret-change-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
   Save: `Ctrl+O`, `Enter`, `Ctrl+X`.
5. Build and start:
```bash
   docker compose up --build -d
   docker compose ps
   docker compose logs app --tail=30
```
   Confirm `Application startup complete.`
6. Access: `http://<public-ip>:8000/docs`
7. **When done, stop the instance** (AWS Console → Instance state → Stop) to avoid charges.

## Issues Faced & Fixes

- **Port 5432 conflict** (Day 29): local Windows PostgreSQL already used port
  5432, so Docker Postgres was mapped to host port `5433` instead, staying
  `5432` internally between containers.
- **JWT "sub" type mismatch** (Day 29): JWT `sub` must be a string
  (`str(user.id)`), but `session.get()` needs an int — fixed with
  `int(user_id)` in `dependencies.py`.
- **SQLAlchemy `MultipleResultsFound`** (Day 30): duplicate rows in
  `project_members` from repeated testing. Fixed with `.scalars().first()`
  instead of `.scalar_one_or_none()`, plus a `UniqueConstraint` in
  `models.py` to prevent future duplicates.
- **Redis event-loop conflict in pytest** (Day 30): global `redis_client`
  reused across tests with different event loops caused
  `RuntimeError: Event loop is closed`. Fixed by wrapping all Redis calls
  in `try/except` — caching becomes best-effort, app never crashes if
  Redis hiccups.
- **Docker permission denied on EC2** (Day 30): `ubuntu` user wasn't in the
  `docker` group. Fixed with `sudo usermod -aG docker ubuntu`, then
  reconnecting SSH.

## Commands Reference

```powershell
# Local
git checkout -b day29-capstone-setup
docker-compose up --build
docker-compose down
docker-compose down -v              # wipes DB data (used after schema change)
docker-compose logs app --tail=50
docker-compose exec app pytest -v

# Git
git add .
git commit -m "message"
git push origin day29-capstone-setup

# AWS
ssh -i "task-api-key.pem" ubuntu@<public-ip>
git fetch origin && git pull origin day29-capstone-setup
docker compose up --build -d
docker compose logs app --tail=30
```

## Final Status
All brief requirements implemented and verified:
Python (modular, OOP, type hints) · SQL (4 tables, FKs, unique constraint,
JOIN) · FastAPI (full CRUD, validation, routers, DI, /docs) · Auth (JWT,
bcrypt, roles, env secrets) · Async/Performance (async endpoints,
pagination/filtering, Redis caching) · Networking (correct REST
methods/codes) · Testing (11/11 pytest passing) · Git (branch, PR, commits)
· Docker (multi-stage + compose) · CI/CD (GitHub Actions, verified passing)
· AWS (EC2, tested live via public IP)
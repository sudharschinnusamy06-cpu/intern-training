# Day 21 - Dockerize the Task API (Combined)

## What I learned
- .dockerignore - excluding files from being copied into Docker images
- This day combines everything from Day 19-20 into one final containerized stack

## Why .dockerignore matters
- Without it, `COPY . .` in the Dockerfile copies EVERYTHING in the folder into the image
- This includes venv/ (huge, unnecessary), __pycache__/ (cache files), .env (secrets!), .git/ (commit history)
- Secrets should never be baked into an image - they're passed at runtime via docker-compose.yml environment section instead

## Folder structure
Day21-dockerize-combined/
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   └── routers/
│       └── tasks.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env (gitignored)
├── requirements.txt
└── README.md

## What's containerized
- api service - FastAPI Task Management API (built from Dockerfile)
- db service - PostgreSQL 17 with persistent volume (pgdata)
- Healthcheck on db ensures api waits until PostgreSQL is truly ready before starting
- Full app↔DB networking via service name (DATABASE_HOST=db)

## Commands used

| Command | Used for |
|---|---|
| `docker compose up --build` | Build and start entire stack (api + db) with one command |
| `docker compose down` | Stop and remove containers (volume + images persist) |

## Result
Entire Task Management API + PostgreSQL database now starts with a single command:
docker compose up --build
No manual PostgreSQL setup, no manual venv activation needed inside containers - fully portable.

## Testing Summary
- Verified GET/POST /tasks work via http://localhost:8080/docs
- Confirmed data persists across `docker compose down` + `up` (volume working)
- Confirmed api waits for db healthcheck before starting (no more connection-refused errors)
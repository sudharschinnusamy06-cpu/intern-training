# Day 20 - Docker Compose (Multi-Container App)

## What I learned
- Why Docker Compose is needed (running multiple containers together)
- Writing a docker-compose.yml file (services, ports, environment, depends_on)
- Connecting containers using service names instead of localhost
- Fixing Python import paths when running app as a package (app.main:app)
- Environment variables passed into containers via .env

## Key concept
- Inside Docker, `localhost` means "this container only" - not other containers, not the host machine
- Containers talk to each other using their service name from docker-compose.yml (e.g. `db`)
- `.env` values are read automatically by Compose using `${VARIABLE_NAME}` syntax

## Folder structure
Day20-docker-compose/
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   └── routers/
│       └── tasks.py
├── Dockerfile
├── docker-compose.yml
├── .env (gitignored)
├── requirements.txt
└── README.md

## Commands used

| Command | Used for |
|---|---|
| `docker compose version` | Verify Docker Compose is installed |
| `pip freeze > requirements.txt` | Generate list of installed Python packages for the Dockerfile to install |
| `docker compose up --build` | Build images (if changed) and start all services defined in docker-compose.yml |
| `docker compose down` | Stop and remove all containers started by Compose (images/volumes stay) |

## Bugs fixed
- `ModuleNotFoundError: No module named 'routers'` / `'auth'` / `'models'` / `'database'`
  - Cause: app runs as a package (`app.main:app`), so internal imports needed `app.` prefix
  - Fixed imports in `main.py`, `tasks.py`, `database.py` to use `from app.xxx import ...`
- Database connection used hardcoded `localhost`
  - Fixed by reading host from `.env` (`DATABASE_HOST`) — `localhost` when run directly, `db` when run via Compose

## Testing Summary
- `docker compose up --build` started both `db` (PostgreSQL) and `api` (FastAPI) containers successfully
- Verified GET /tasks and POST /tasks (with API key) work via http://localhost:8080/docs
- Confirmed FastAPI container connects to PostgreSQL container using service name `db`, not localhost
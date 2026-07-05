# Day 17 - FastAPI + SQL (Combined)

## What I Learned
- SQLModel - combines Pydantic validation + SQLAlchemy ORM
- Connecting FastAPI to PostgreSQL (interndb)
- Creating real database tables from Python classes
- Database sessions and dependency injection (Depends(get_session))
- Full CRUD now persists permanently (survives server restart)

## Structure
- database.py - engine, session, table creation
- models.py - Task table definition
- routers/tasks.py - CRUD endpoints using DB session
- main.py - creates app, includes router, creates tables on startup

## Setup Commands Used

### Install SQLModel
pip install sqlmodel

### Database Connection (database.py)
Connection string format used to connect Python to PostgreSQL:
postgresql://postgres:<password>@localhost:5432/interndb

### Run the server
cd Day17-fastapi-sql
uvicorn main:app --reload

### Verify table creation (psql method)
$env:PATH += ";C:\Program Files\PostgreSQL\17\bin"
psql -U postgres -d interndb
\dt
\d task

### Verify table creation (pgAdmin method)
- Open pgAdmin → Servers → PostgreSQL 17 → Databases → interndb → Schemas → public → Tables
- Confirmed `task` table appeared automatically with columns: id, title, description, completed

## Key Milestone
- Task API data now survives server restarts
- Verified via pgAdmin - task table with real data
- Replaced Day 15/16's in-memory storage with real PostgreSQL persistence

## Security Note (to fix later - Day 27)
- Database password currently hardcoded in database.py
- Should move to .env file with proper secrets management
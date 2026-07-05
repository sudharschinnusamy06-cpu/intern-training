# Day 18 - Auth & Middleware

## What I Learned
- Dependency injection for authentication (Depends pattern)
- Simple API key authentication using request headers
- Environment variables (.env) for secrets management
- CORS middleware - allows cross-origin requests
- Custom logging middleware - logs every incoming request

## Structure
- .env - stores DATABASE_PASSWORD and API_KEY (gitignored)
- auth.py - verify_api_key() dependency function
- database.py - now reads password from .env instead of hardcoding
- routers/tasks.py - POST/PUT/DELETE protected with API key; GET stays public
- main.py - CORS + logging middleware added

## Setup Commands Used

### Install python-dotenv
pip install python-dotenv
Used to read secret values (DB password, API key) from the .env file into Python.

### .env file content (not pushed to GitHub - gitignored)
DATABASE_PASSWORD=your_password
API_KEY=your_secret_key

### Run the server
cd Day18-auth-middleware
uvicorn main:app --reload

### Test authentication (via /docs)
- POST /tasks without x-api-key header → blocked (422/401 error)
- POST /tasks with correct x-api-key header → 200 OK, task created

### Verify logging middleware
- Every request to the server now prints in terminal:
Incoming request: GET http://127.0.0.1:8000/tasks

## Security Improvement
- Fixed Day 17's flagged issue: DB password moved from hardcoded to .env
- Write operations (create/update/delete) now require valid X-API-Key header
- Read operations (GET) remain public

## Testing Summary
- Verified POST without API key → blocked
- Verified POST with correct API key → 200 OK, task created
- Verified CORS middleware active (no startup errors)
- Verified logging middleware prints every request

## Note for later (Day 27)
- Current auth is a simple API key - full JWT with login/password/hashing comes in Day 27
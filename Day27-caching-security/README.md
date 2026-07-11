# Day 27 - Caching, Security & Performance

## What I learned
- Redis as an in-memory cache — skip re-querying DB for repeated requests
- Rate limiting with slowapi — block a user after too many requests/minute
- Circular imports in Python — fixed by moving shared objects to their own file
- Password hashing (bcrypt/passlib) — never store real passwords
- JWT tokens — per-user login with expiry, replacing a single shared API key
- Docker Compose only passes env vars explicitly listed under each service
- SQLModel's query builder is SQL-injection-safe by default

## What I did
1. Added Redis caching to GET /tasks (30s expiry), verified via redis-cli
2. Added rate limiting (5/min) to GET /tasks, verified via 429 response
3. Fixed circular import (main.py <-> tasks.py) by creating rate_limiter.py
4. Added bcrypt hashing + JWT create/verify functions to auth.py
5. Created User model + users.py router (/register, /login)
6. Replaced API-key auth with JWT auth on create/update/delete task routes
7. Fixed 3 real bugs: bcrypt version conflict, missing SECRET_KEY in docker-compose, accidentally replaced router include line
8. Verified full login flow via curl.exe (Swagger UI had a header quirk)
9. Updated all tests to use JWT tokens; added register/login tests
10. Reviewed OWASP basics: SQL injection safe, CORS wide open (noted), logging already in place

## Results
- 21/21 tests passing, 95% coverage
- Redis caching, rate limiting, and JWT auth all verified working (redis-cli, 429 response, curl)

## Known issues (not fixed today)
- Swagger UI doesn't reliably send manual Authorization headers — tested via curl.exe instead; proper fix is OAuth2PasswordBearer
- CORS wide open (allow_origins=["*"]) — fine for dev, not production
- datetime.utcnow() deprecation warning — still works, minor cleanup later
- Old verify_api_key() function unused but not deleted

## Key commands
| Command | Purpose |
|---|---|
| docker exec -it <redis-container> redis-cli | Inspect cached keys |
| curl.exe -X POST "..." -H "authorization: Bearer <token>" -d "@body.json" | Test JWT-protected routes |
| pip install "bcrypt==4.0.1" | Fix bcrypt/passlib compatibility |
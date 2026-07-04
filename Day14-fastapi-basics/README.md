# Day 14 - FastAPI Basics

## What I Learned
- FastAPI + uvicorn setup
- Creating GET endpoints
- Path parameters (e.g., /employee/{employee_id})
- Query parameters (e.g., /employees?department=IT)
- Auto-generated docs at /docs

## Endpoints Built
- GET / - health check
- GET /employee/{employee_id}
- GET /employee/{employee_id}/details
- GET /employees (query param: department)
- GET /employees/search (query params: name, min_salary)
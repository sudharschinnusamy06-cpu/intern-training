# Day 16 - App Structure & CRUD

## What I Learned
- APIRouter for organizing routes into separate files
- Modular structure: models.py, routers/, main.py
- Proper error handling with HTTPException (404 Not Found)
- app.include_router() to connect routers to main app

## Structure
- models.py - Item Pydantic model
- routers/items.py - all CRUD endpoints
- main.py - creates app, includes router

## Improvement over Day 15
- Same functionality, but organized into separate files
- Added proper 404 errors instead of 500 crashes
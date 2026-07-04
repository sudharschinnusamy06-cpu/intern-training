# Day 15 - Request Bodies & Pydantic

## What I Learned
- POST/PUT/DELETE HTTP methods
- Request bodies (data sent to server, not in URL)
- Pydantic models (BaseModel) for automatic data validation
- In-memory storage limitations (data resets on server reload)

## Endpoints Built (Full CRUD)
- POST /items - create item
- GET /items - list all items
- GET /items/{item_id} - get one item
- PUT /items/{item_id} - update item
- DELETE /items/{item_id} - delete item

## Model
Item(BaseModel): name (str), price (float), quantity (int)
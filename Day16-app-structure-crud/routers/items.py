from fastapi import APIRouter, HTTPException
from models import Item

router = APIRouter()

items = []

@router.post("/items")
def create_item(item: Item):
    items.append(item)
    return {"message": "Item created", "item": item}

@router.get("/items")
def get_items():
    return items

@router.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id >= len(items) or item_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@router.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id >= len(items) or item_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return {"message": "Item updated", "item": item}

@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id >= len(items) or item_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items.pop(item_id)
    return {"message": "Item deleted", "item": deleted_item}

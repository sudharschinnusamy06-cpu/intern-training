from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    quantity: int

items = []

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return {"message": "Item created", "item": item}

@app.get("/items")
def get_items():
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return items[item_id]

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    items[item_id] = item
    return {"message": "Item updated", "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    deleted_item = items.pop(item_id)
    return {"message": "Item deleted", "item": deleted_item}
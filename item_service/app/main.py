from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import SessionLocal, engine
from app import models
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lost & Found Item Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def try_match_item(new_item, db):
    opposite_status = "FOUND" if new_item.status == "LOST" else "LOST"

    match = db.query(models.Item).filter(
        models.Item.item_name.ilike(new_item.item_name),
        models.Item.location == new_item.location,
        models.Item.status == opposite_status
    ).first()

    if match:
        new_item.status = "MATCHED"
        match.status = "MATCHED"
        db.commit()

# ---------- DB Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Schemas ----------
class ItemRequest(BaseModel):
    item_name: str
    description: str
    location: str
    user_id: int

# ---------- Routes ----------
@app.post("/lost-item")
def report_lost_item(item: ItemRequest, db: Session = Depends(get_db)):
    lost_item = models.Item(
        item_name=item.item_name,
        description=item.description,
        location=item.location,
        status="LOST",
        user_id=item.user_id
    )

    db.add(lost_item)
    db.commit()
    db.refresh(lost_item)

    try_match_item(lost_item, db)

    return {"message": "Lost item reported successfully"}


@app.post("/found-item")
def report_found_item(item: ItemRequest, db: Session = Depends(get_db)):
    found_item = models.Item(
        item_name=item.item_name,
        description=item.description,
        location=item.location,
        status="FOUND",
        user_id=item.user_id
    )

    db.add(found_item)
    db.commit()
    db.refresh(found_item)

    try_match_item(found_item, db)

    return {"message": "Found item reported successfully"}


@app.get("/items")
def get_all_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@app.get("/items/user/{user_id}")
def get_items_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Item).filter(models.Item.user_id == user_id).all()

@app.put("/items/{item_id}/returned")
def mark_item_returned(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not item:
        return {"error": "Item not found"}

    item.status = "RETURNED"
    db.commit()

    return {"message": "Item marked as returned"}


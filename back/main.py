from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from typing import ItemsView, List
from . import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=List[schemas.Item])
async def read_items(skip: int = 0, limit: int = 1001, db: Session = Depends(get_db)):
    items = crud.get_keys(db, skip=skip, limit=limit)

    return items

@app.post("/", response_model=schemas.Item)
async def create_items(item: List[schemas.Item], db: Session = Depends(get_db)):
    return crud.insert_key(db=db, items=item)
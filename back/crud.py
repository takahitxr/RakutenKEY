from requests import Session
from sqlalchemy.orm import session
from . import models, schemas

def get_keys(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Item).offset(skip).limit(limit).all()


def insert_key(db:Session, items:schemas.Item):
    db_Item = [models.Item(
        keyword = item.keyword,
        rank = item.rank,
    )for item in items]

    db.add_all(db_Item)
    db.commit()
 #   db.refresh(db_Item)
    return db_Item
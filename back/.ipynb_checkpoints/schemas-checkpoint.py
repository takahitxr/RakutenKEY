from argparse import ONE_OR_MORE
import datetime
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    keyword: str
    rank: int
    date = datetime.date

    class Config:
        orm_mode = True

from argparse import ONE_OR_MORE
import datetime
from pydantic import BaseModel
from typing import ItemsView, List

class Item(BaseModel):
    keyword: str
    rank: int

    class Config:
        orm_mode = True
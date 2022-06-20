from sqlalchemy import Column, DateTime, Integer, String, DATETIME
from traitlets import default
from .database import Base
import datetime

class Item(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True)
    rank = Column(Integer, index=True)
    date = Column(String, index=True, default=datetime.date.today().strftime('%Y/%M/%D'))
    
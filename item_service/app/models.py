from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    description = Column(String)
    location = Column(String, nullable=False)
    status = Column(String, nullable=False)  # LOST / FOUND
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

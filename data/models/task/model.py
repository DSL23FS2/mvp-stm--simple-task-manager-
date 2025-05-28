# data/models/task/model.py
from data.base_metadata import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean 
from datetime import datetime, timezone

def time_utc():
    return datetime.now(timezone.utc)

class ModelTask(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=time_utc)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    is_completed = Column(Boolean, nullable=False, default=False)  

    def __repr__(self):
        return f"<ModelTask(id={self.id}, name={self.name}, created_at={self.created_at})>"

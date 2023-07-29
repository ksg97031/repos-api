from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, JSON
from sqlalchemy.sql import func
from app.database import Base

class Org(Base):
    __tablename__ = 'org'
    name = Column(String, primary_key=True, index=True)
    repos = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
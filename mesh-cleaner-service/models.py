from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, JSON
from database import Base


class MeshLog(Base):
    __tablename__ = "mesh_logs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    mesh_stats = Column(JSON, nullable=False)
    bounding_box = Column(JSON, nullable=True)
    logs = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

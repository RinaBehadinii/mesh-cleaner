from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from database import Base


class MeshLog(Base):
    __tablename__ = "mesh_logs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)

    input_vertices = Column(Integer)
    output_vertices = Column(Integer)
    input_faces = Column(Integer)
    output_faces = Column(Integer)

    bounding_box_before = Column(JSON, nullable=True)
    bounding_box_after = Column(JSON, nullable=True)

    logs = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

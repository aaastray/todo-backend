from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid

from src.db.database import Base

class ToDo(Base):
    __tablename__ = 'todos'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    completed = Column(Boolean, default=False)
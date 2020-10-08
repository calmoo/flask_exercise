from sqlalchemy import Column, Integer, String
from .database import Base


class Todo(Base):
    __tablename__ = "Todos"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    text = Column(String(), nullable=False)
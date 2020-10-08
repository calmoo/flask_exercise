from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Todo(Base):
    __tablename__ = "Todos"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    text = Column(String(), nullable=False)
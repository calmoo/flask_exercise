from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_bcrypt import generate_password_hash, check_password_hash
from typing import Any

Base = declarative_base()


class Todo(Base):
    __tablename__ = "Todos"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    text = Column(String(), nullable=False)
    owner = Column(Integer, ForeignKey("users.id"))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    todos = relationship("Todo")

    def hash_password(self) -> None:
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password: str) -> Any:
        return check_password_hash(self.password, password)

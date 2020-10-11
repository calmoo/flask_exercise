from argon2.exceptions import VerifyMismatchError
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from argon2 import PasswordHasher

Base = declarative_base()
ph = PasswordHasher()


class Todo(Base):
    __tablename__ = "Todos"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    text = Column(String(), nullable=False)
    owner = Column(Integer, ForeignKey("Users.id"))


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    todos = relationship("Todo")

    def hash_password(self) -> None:
        self.password = ph.hash(self.password)

    def check_password(self, password: str) -> bool:
        try:
            ph.verify(self.password, password)
            return True
        except VerifyMismatchError:
            return False

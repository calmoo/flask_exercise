from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import generate_password_hash, check_password_hash

Base = declarative_base()


class Todo(Base):
    __tablename__ = "Todos"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    text = Column(String(), nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    def hash_password(self) -> str:
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
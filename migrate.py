from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv; load_dotenv()

Base = declarative_base()
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    deepl_key = Column(String(100), nullable=False)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
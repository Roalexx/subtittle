import os, bcrypt, re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv; load_dotenv()
from migrate import User, Base  

ENGINE = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=ENGINE)

_pwd_re = re.compile(r"^(?=.*\d)[A-Za-z\d]{8,}$")

def hash_pw(plain):
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def check_pw(plain, hashed):
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def valid_pw(pw):
    return bool(_pwd_re.fullmatch(pw))
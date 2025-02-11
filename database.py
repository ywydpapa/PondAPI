from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import dotenv
import os

dotenv.load_dotenv()
DBHOST = os.getenv("dbhost")
DBUSER = os.getenv("dbuser")
DBPASS = os.getenv("userpass")
DBNAME = os.getenv("dbname")

DATABASE_URL = "mysql+pymysql://"+DBUSER+":"+DBPASS+"@"+DBHOST+":3306/"+DBNAME

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
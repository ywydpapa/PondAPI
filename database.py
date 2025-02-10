from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

DATABASE_URL = "mysql+pymysql://user:sqjfrl@swc9004.ipg:3306/cnd"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

database = Database(DATABASE_URL)

Base = declarative_base()

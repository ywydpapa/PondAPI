from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "pondUser"

    userNo = Column(Integer, primary_key=True, index=True)
    userId = Column(String(100), index=True)
    userName = Column(String(100), unique=True, index=True)

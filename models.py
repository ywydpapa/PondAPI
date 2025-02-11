from sqlalchemy import MetaData
from database import engine, Base

metadata = MetaData()
metadata.reflect(bind=engine)  # 기존 테이블 자동 로드

class User(Base):
    __table__ = metadata.tables["traceUser"]

class Setups(Base):
    __table__ = metadata.tables["tradingSetup"]

class Result(Base):
    __table__ = metadata.tables["tradeResult"]
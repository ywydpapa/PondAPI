from sqlalchemy import MetaData
from database import engine, Base

metadata = MetaData()
metadata.reflect(bind=engine)  # 기존 테이블 자동 로드

class User(Base):
    __table__ = metadata.tables["traceUser"]

class Setups(Base):
    __table__ = metadata.tables["traceSetup"]

class Sets(Base):
    __table__ = metadata.tables["traceSets"]

class Result(Base):
    __table__ = metadata.tables["tradeResult"]

class Board(Base):
    __table__ = metadata.tables["board"]

class Errors(Base):
    __table__ = metadata.tables["error_Log"]

class Service(Base):
    __table__ = metadata.tables["service_Log"]

class Server(Base):
    __table__ = metadata.tables["serverSet"]

class ServiceStat(Base):
    __table__ = metadata.tables["service_Stat"]

class Losscut(Base):
    __table__ = metadata.tables["lcLog"]
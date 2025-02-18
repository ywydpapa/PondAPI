from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, Setups, Result, Sets, Losscut
from typing import List, Optional
from schemas import UserResponse, SetupResponse, ResultResponse, UserkeyResponse, SetsResponse, LosscutResponse

app = FastAPI()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 모든 사용자 조회 API (전체 조회)
@app.get("/users", response_model=List[UserResponse])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/userkey/{userNo}", response_model=List[UserkeyResponse])
def read_users(userNo: int, db: Session = Depends(get_db)):
    userkey = db.query(User).filter(User.userNo == userNo).all()
    return userkey

@app.get("/setup", response_model=List[SetupResponse])
def read_setups(db: Session = Depends(get_db)):
    setups = db.query(Setups).filter(Setups.attrib.not_like(f"%XXXUP%")).all()
    return setups

@app.get("/sets/{setNo}", response_model=List[SetsResponse])
def read_sets(setNo : int, db: Session = Depends(get_db)):
    sets = db.query(Sets).filter(Sets.setNo == setNo).all()
    return sets

@app.get("/setup/{userNo}", response_model=List[SetupResponse])
def user_setups(userNo: int, db: Session = Depends(get_db)):
    setups = db.query(Setups).filter(Setups.attrib.not_like(f"%XXXUP%"), Setups.userNo == userNo ).all()
    return setups

@app.get("/myresult/{userNo}", response_model=List[ResultResponse])
def myresults(userNo: int , db: Session = Depends(get_db)):
    setups = db.query(Result).filter(Result.userNo == userNo).all()
    return setups


@app.get("/losscuts/{userNo}", response_model=List[LosscutResponse])
def losscuts(userNo: int, db: Session = Depends(get_db)):
    items = db.query(Losscut).filter(Losscut.userNo == userNo).all()
    return items


# 특정 사용자 조회 (조건: ID)
@app.get("/users/{userNo}", response_model=UserResponse)
def read_user_by_id(userNo: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(userNo == userNo).first()
    if user is None:
        return {"error": "User not found"}
    return user

# 특정 사용자 검색 (이름, 이메일로 조회)
@app.get("/users/search", response_model=List[UserResponse])
def search_users(
    userName: Optional[str] = Query(None),
    userId: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(User)

    if userName:
        query = query.filter(User.userName.like(f"%{userName}%"))
    if userId:
        query = query.filter(User.userId == userId)

    users = query.all()
    return users

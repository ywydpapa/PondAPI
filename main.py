from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

# Pydantic 스키마 정의
class UserResponse(BaseModel):
    userNo: int
    userId: str
    userName: str

    class Config:
        orm_mode = True

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

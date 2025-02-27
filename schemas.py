from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserResponse(BaseModel):
    userNo: int
    userId: str
    userName: str

class UserkeyResponse(BaseModel):
    userNo : int
    apiKey1 : str
    apiKey2 : str
    setupKey : int

class SetupResponse(BaseModel):
    setupNo : int
    userNo : int
    initAsset : float
    bidInterval : int
    bidRate : float
    askRate : float
    bidCoin : str
    activeYN : Optional[str] = "N"
    custKey : str
    serverNo : int
    holdYN : str
    holdNo : int
    doubleYN : str
    limitYN : str
    limitAmt : float
    slot : int
    regDate : datetime
    attrib : str

class SetsResponse(BaseModel):
    setNo : int
    setTitle : str
    setInterval : int
    step0 : float
    step1 : float
    step2 : float
    step3 : float
    step4 : float
    step5 : float
    step6 : float
    step7 : float
    step8 : float
    step9 : float
    inter0 : float
    inter1 : float
    inter2 : float
    inter3 : float
    inter4 : float
    inter5 : float
    inter6 : float
    inter7 : float
    inter8 : float
    inter9 : float
    bid0 : float
    bid1 : float
    bid2 : float
    bid3 : float
    bid4 : float
    bid5 : float
    bid6 : float
    bid7 : float
    bid8 : float
    bid9 : float
    max0 : float
    max1 : float
    max2 : float
    max3 : float
    max4 : float
    max5 : float
    max6 : float
    max7 : float
    max8 : float
    max9 : float
    useYN : Optional[str]
    regDate : datetime
    attrib : str

class ResultResponse(BaseModel):
    userNo : int
    coinName :str
    balance : float
    avgPrice : float
    amt :float
    regDate : datetime
    attrib :str


class LosscutResponse(BaseModel):
    lcNo : int
    userNo : int
    lcCoinn : str
    lcGap : float
    regDate : datetime
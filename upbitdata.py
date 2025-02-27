import pyupbit
import numpy as np

def getCoinn():
    try:
        coins = pyupbit.get_tickers(fiat = "KRW")
        print(coins)
    except Exception as e:
        print("코인 목록 조회 에러",e)
    finally:
        return coins

def getCurrPrice(coinn):
    try:
        curprice = pyupbit.get_current_price(coinn)
        print(curprice)
    except Exception as e:
        print("현재가 조회 에러",e)
    finally:
        return curprice

def getCandle1m2h(coinn):
    try:
        candles = pyupbit.get_ohlcv(coinn, interval="minute1", count=120)
        print(candles)
    except Exception as e:
        print("캔들차트 1분 조회 에러 ",e)
    finally:
        return candles

def getCandle3m2h(coinn):
    try:
        candles = pyupbit.get_ohlcv(coinn, interval="minute3", count=40)
        print(candles)
    except Exception as e:
        print("캔들차트 3분 조회 에러 ",e)
    finally:
        return candles

def getCandle5m2h(coinn):
    try:
        candles = pyupbit.get_ohlcv(coinn, interval="minute5", count=24)
        print(candles)
    except Exception as e:
        print("캔들차트 5분 조회 에러 ",e)
    finally:
        return candles

def getCandle15m2h(coinn):
    try:
        candles = pyupbit.get_ohlcv(coinn, interval="minute15", count=8)
        print(candles)
    except Exception as e:
        print("캔들차트 15분 조회 에러 ",e)
    finally:
        return candles

def getCandle30m2h(coinn):
    try:
        candles = pyupbit.get_ohlcv(coinn, interval="minute30", count=4)
        print(candles)
    except Exception as e:
        print("캔들차트 30분 조회 에러 ",e)
    finally:
        return candles

def getOrderbook(coinn):
    try:
        orderbook = pyupbit.get_orderbook(coinn)
        print(orderbook)
    except Exception as e:
        print ("오더북 조회 에러",e)
    finally:
        return orderbook


getCandle1m2h("KRW-ETH")


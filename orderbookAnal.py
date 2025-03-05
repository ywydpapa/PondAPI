import requests
import psycopg2

def get_orderbook(market):
    url = "https://api.upbit.com/v1/orderbook"
    params = {"markets": market}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

# PostgreSQL 연결 정보 설정
DB_CONFIG = {
    "dbname": "your_db",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": 5432
}

def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

# 테스트 실행a
orderbooks = get_orderbook("KRW-XRP")
for orderbook in orderbooks:
    orders = orderbook["orderbook_units"]
    for order in orders:
        print(orderbook["market"], end=" ")
        print(orderbook["timestamp"], end=" ")
        totalask =orderbook["total_ask_size"]
        totalbid = orderbook["total_bid_size"]
        print(order, end= ' ASK Rate ')
        print(round(order['ask_size']/ totalask * 100, 3), end= ' Bid Rate ')
        print(round(order['bid_size']/ totalbid * 100,3))

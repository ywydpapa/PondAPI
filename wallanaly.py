import requests
import pandas as pd

def get_upbit_trade_strength_and_orderbook_details(market="KRW-BTC", count=200):
    # 1. 체결 데이터 가져오기 (최신 100개)
    url_trades = f"https://api.upbit.com/v1/trades/ticks?market={market}&count={count}"
    headers = {"Accept": "application/json"}
    response_trades = requests.get(url_trades, headers=headers)

    if response_trades.status_code != 200:
        print("체결 데이터 API 요청 실패:", response_trades.status_code)
        return None

    trades = response_trades.json()

    # 2. 체결 데이터 DataFrame 변환 및 한국시간(KST) 변환
    df = pd.DataFrame(trades)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)  # UTC 변환
    df['timestamp'] = df['timestamp'].dt.tz_convert('Asia/Seoul')  # KST 변환
    df['minute'] = df['timestamp'].dt.strftime('%H:%M')  # 시:분 단위 변환

    # 3. 체결 데이터를 분 단위로 그룹화하여 체결강도 계산
    grouped = df.groupby('minute').agg(
        buy_volume=('trade_volume', lambda x: x[df['ask_bid'] == 'BID'].sum()),
        sell_volume=('trade_volume', lambda x: x[df['ask_bid'] == 'ASK'].sum())
    ).reset_index()

    grouped['trade_strength'] = (grouped['buy_volume'] / (grouped['buy_volume'] + grouped['sell_volume'])) * 100
    grouped['trade_strength'] = grouped['trade_strength'].fillna(0)  # NaN 방지

    # 4. 호가 데이터 가져오기
    url_orderbook = f"https://api.upbit.com/v1/orderbook?markets={market}"
    response_orderbook = requests.get(url_orderbook, headers=headers)

    if response_orderbook.status_code != 200:
        print("호가 데이터 API 요청 실패:", response_orderbook.status_code)
        return None

    orderbook = response_orderbook.json()[0]  # 첫 번째 데이터 (market이 하나일 경우)

    # 5. 가격대별 매수벽(Bid Wall)과 매도벽(Ask Wall) 계산
    bid_walls = []  # 매수벽: 각 가격대별 매수 주문량
    ask_walls = []  # 매도벽: 각 가격대별 매도 주문량

    for unit in orderbook['orderbook_units']:
        bid_walls.append({
            'price': unit['bid_price'],
            'quantity': unit['bid_size']
        })
        ask_walls.append({
            'price': unit['ask_price'],
            'quantity': unit['ask_size']
        })

    # 6. 가장 큰 매수벽과 매도벽 찾기
    max_bid_wall = max(bid_walls, key=lambda x: x['quantity'])  # 가장 큰 매수벽
    max_ask_wall = max(ask_walls, key=lambda x: x['quantity'])  # 가장 큰 매도벽

    # 7. 매수벽과 매도벽의 비율
    total_bid_wall = sum([unit['quantity'] for unit in bid_walls])
    total_ask_wall = sum([unit['quantity'] for unit in ask_walls])

    bid_to_ask_ratio = (total_bid_wall / total_ask_wall) if total_ask_wall > 0 else 0

    return grouped[['minute', 'trade_strength']], bid_walls, ask_walls, max_bid_wall, max_ask_wall, bid_to_ask_ratio

# 📌 사용 예제
market = "KRW-XRP"
strength_by_time, bid_walls, ask_walls, max_bid_wall, max_ask_wall, bid_to_ask_ratio = get_upbit_trade_strength_and_orderbook_details(market)

print("📊 분별 체결강도:")
print(strength_by_time)
print(f"\n💎 가장 큰 매수벽 (Bid Wall): {max_bid_wall['price']} 원 / {max_bid_wall['quantity']} / {round(max_bid_wall['price']*max_bid_wall['quantity'],2)} {market}")
print(f"🔥 가장 큰 매도벽 (Ask Wall): {max_ask_wall['price']} 원 / {max_ask_wall['quantity']} / {round(max_ask_wall['price']*max_ask_wall['quantity'],2)} {market}")
print(f"\n📉 매수벽과 매도벽 비율 (Bid:Ask): {bid_to_ask_ratio:.2f}")

# 📑 가격대별 매수벽과 매도벽 출력
print("\n📈 매수벽 상세 (가격대별):")
for bid in bid_walls:
    print(f"가격: {bid['price']} 원 / 매수량: {bid['quantity']} {market}")

print("\n📉 매도벽 상세 (가격대별):")
for ask in ask_walls:
    print(f"가격: {ask['price']} 원 / 매도량: {ask['quantity']} {market}")

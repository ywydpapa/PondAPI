import requests
import pandas as pd

def get_upbit_trade_strength_and_orderbook(market="KRW-BTC", count=100):
    # 1. 체결 데이터 가져오기 (최근 100개)
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

    # 5. 매수벽(Bid Wall)과 매도벽(Ask Wall) 계산
    bid_wall = sum(unit['bid_size'] for unit in orderbook['orderbook_units'])  # 매수 대기량 합계
    ask_wall = sum(unit['ask_size'] for unit in orderbook['orderbook_units'])  # 매도 대기량 합계

    return grouped[['minute', 'trade_strength']], bid_wall, ask_wall

# 📌 사용 예제
market = "KRW-XRP"
strength_by_time, bid_wall, ask_wall = get_upbit_trade_strength_and_orderbook(market)

print("📊 분별 체결강도:")
print(strength_by_time)
print(f"\n💎 매수벽 (Bid Wall): {bid_wall:.2f} {market}")
print(f"🔥 매도벽 (Ask Wall): {ask_wall:.2f} {market}")

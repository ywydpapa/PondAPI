import requests
import pandas as pd

def get_upbit_trade_strength_by_time(market="KRW-BTC", count=400):
    # 1. 업비트 API 요청 (최신 100개 체결 데이터 가져오기)
    url = f"https://api.upbit.com/v1/trades/ticks?market={market}&count={count}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("API 요청 실패:", response.status_code)
        return None

    trades = response.json()

    # 2. DataFrame 변환 및 한국시간(KST) 변환
    df = pd.DataFrame(trades)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)  # UTC 기준 변환
    df['timestamp'] = df['timestamp'].dt.tz_convert('Asia/Seoul')  # 한국 시간(KST) 변환
    df['minute'] = df['timestamp'].dt.strftime('%H:%M')  # '시:분' 형식으로 변환

    # 3. 매수(BID)와 매도(ASK) 체결량 집계
    grouped = df.groupby('minute').agg(
        buy_volume=('trade_volume', lambda x: x[df['ask_bid'] == 'BID'].sum()),
        sell_volume=('trade_volume', lambda x: x[df['ask_bid'] == 'ASK'].sum())
    ).reset_index()

    # 4. 체결강도 계산
    grouped['trade_strength'] = (grouped['buy_volume'] / (grouped['buy_volume'] + grouped['sell_volume'])) * 100
    grouped['trade_strength'] = grouped['trade_strength'].fillna(0)  # NaN 방지

    return grouped[['minute', 'trade_strength']]


# 📌 사용 예제
market = "KRW-XRP"
strength_by_time = get_upbit_trade_strength_by_time(market)

print(strength_by_time)

import requests


def get_upbit_trade_strength(market="KRW-BTC", count=100):
    # 1. API 요청 (한 번만 실행)
    url = f"https://api.upbit.com/v1/trades/ticks?market={market}&count={count}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("API 요청 실패:", response.status_code)
        return None, None

    trades = response.json()

    # 2. 최근 50개 및 100개 데이터 나누기
    trades_10 = trades[:10]  # 최근 50개
    trades_50 = trades[:50]  # 최근 50개
    trades_100 = trades  # 최근 100개 (전체)

    # 3. 체결강도 계산 함수
    def calculate_strength(trades_subset):
        buy_volume = sum(trade['trade_volume'] for trade in trades_subset if trade['ask_bid'] == 'BID')
        sell_volume = sum(trade['trade_volume'] for trade in trades_subset if trade['ask_bid'] == 'ASK')
        total_volume = buy_volume + sell_volume
        return (buy_volume / total_volume) * 100 if total_volume > 0 else 0.0

    # 4. 두 개의 count 값에 대한 체결강도 계산
    strength_10 = calculate_strength(trades_10)
    strength_50 = calculate_strength(trades_50)
    strength_100 = calculate_strength(trades_100)

    return strength_10, strength_50, strength_100


# 📌 사용 예제
market = "KRW-XRP"
strength_10, strength_50, strength_100 = get_upbit_trade_strength(market, count=100)
print(f"{market} 체결강도 (최근 10개 데이터): {strength_10:.2f}%")
print(f"{market} 체결강도 (최근 50개 데이터): {strength_50:.2f}%")
print(f"{market} 체결강도 (최근 100개 데이터): {strength_100:.2f}%")

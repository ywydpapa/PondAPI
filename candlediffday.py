import requests
import pandas as pd

def get_candles(market, days):
    # 업비트 API 엔드포인트
    url = "https://api.upbit.com/v1/candles/days"

    # 요청할 데이터 (BTC/KRW 예시)
    params = {
        "market": market,  # 원하는 코인 시장 (ex: KRW-BTC)
        "count": days  # 최근 10일치 데이터
    }
    # API 요청
    response = requests.get(url, params=params)
    data = response.json()
    # 데이터프레임 변환
    df = pd.DataFrame(data)
    # 필요한 컬럼 선택
    df = df[['candle_date_time_kst', 'opening_price', 'high_price', 'low_price', 'trade_price']]
    return df

df = get_candles("KRW-ETH",7)
# 변화폭 계산 (고가 - 저가)
df['change_range'] = df['high_price'] - df['low_price']

# 변화폭 계산 (시가 - 고가)
df['change_rangeoh'] = df['opening_price'] - df['high_price']

# 변화폭 계산 (시가 - 저가)
df['change_rangeol'] = df['opening_price'] - df['low_price']

# 변화폭 계산 (종가 - 고가)
df['change_rangeth'] = df['trade_price'] - df['high_price']

# 변화폭 계산 (종가 - 저가)
df['change_rangetl'] = df['trade_price'] - df['low_price']

#변화율 계산
df['change_rate'] = (df['high_price'] - df['low_price']) / df['low_price'] * 100
# 출력
print(df[['candle_date_time_kst', 'change_range', 'change_rate', 'change_rangeoh','change_rangeol', 'change_rangeth', 'change_rangetl']])

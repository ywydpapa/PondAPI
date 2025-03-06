import requests
import pandas as pd

def get_candles(market, hours):
    # 업비트 API 엔드포인트
    url = "https://api.upbit.com/v1/candles/minutes/60"

    # 요청할 데이터 (BTC/KRW 예시)
    params = {
        "market": market,  # 원하는 코인 시장 (ex: KRW-BTC)
        "count": hours  # 최근 10일치 데이터
    }
    # API 요청
    response = requests.get(url, params=params)
    data = response.json()
    # 데이터프레임 변환
    df = pd.DataFrame(data)
    # 필요한 컬럼 선택
    df = df[['candle_date_time_kst', 'opening_price', 'high_price', 'low_price', 'trade_price']]
    return df

df = get_candles("KRW-BTC",72)
# 방향 계산
df['change_signal'] = df['trade_price'] - df['opening_price']

# 변화폭 계산 (고가 - 저가)
df['change_range'] = (df['high_price'] - df['low_price'])

#변화율 계산
df['change_rate'] = (df['trade_price'] - df['opening_price']) / df['trade_price'] * 100

#방향 계산
df["change_symbol"] = df["change_signal"].apply(lambda x: "+" if x > 0 else "-" if x < 0 else "0")

#방향수 계산
symbol_cnt = df["change_symbol"].value_counts().reindex(["+","-","0"], fill_value=0)

# 출력
print(df[['candle_date_time_kst', 'trade_price', 'change_range', 'change_rate', 'change_symbol']])
print(symbol_cnt)
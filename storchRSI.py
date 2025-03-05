import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


# 한글 폰트 설정 (Windows에서는 'Malgun Gothic', macOS에서는 'AppleGothic', Linux는 'NanumGothic'을 사용할 수 있습니다)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'  # Windows에서 한글 폰트 설정
matplotlib.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨지는 문제 해결

# 업비트에서 OHLCV 데이터 가져오기
def get_upbit_ohlcv(market="KRW-BTC", interval="1", count=200):
    url = f"https://api.upbit.com/v1/candles/minutes/{interval}?market={market}&count={count}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"API 요청 실패: {response.status_code} - {response.text}")
        return None

    ohlcv = response.json()
    df = pd.DataFrame(ohlcv)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df['timestamp'] = df['timestamp'].dt.tz_convert('Asia/Seoul')
    return df


# RSI 계산 함수
def calculate_rsi(df, period=14):
    delta = df['trade_price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def plot_stoch_rsi(df):
    plt.figure(figsize=(14, 8))

    # RSI와 STOCH RSI를 같은 그래프에 그리기
    plt.subplot(2, 1, 1)
    plt.plot(df['timestamp'], df['RSI'], label='RSI', color='blue', alpha=0.7)
    plt.title('RSI & STOCH RSI')
    plt.xlabel('시간')
    plt.ylabel('RSI 값')
    plt.legend(loc='upper left')

    # STOCH RSI 그래프 그리기
    plt.subplot(2, 1, 2)
    plt.plot(df['timestamp'], df['STOCH_RSI'], label='STOCH RSI', color='red', alpha=0.7)
    plt.axhline(y=0.8, color='g', linestyle='--', label='Overbought')
    plt.axhline(y=0.2, color='r', linestyle='--', label='Oversold')
    plt.title('STOCH RSI')
    plt.xlabel('시간')
    plt.ylabel('STOCH RSI 값')
    plt.legend(loc='upper left')

    # 그래프의 날짜 포맷 조정
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# STOCH RSI 계산 함수
def calculate_stoch_rsi(df, rsi_period=14, stoch_rsi_period=14):
    # RSI 계산
    df['RSI'] = calculate_rsi(df, period=rsi_period)

    # STOCH RSI 계산
    df['RSI_max'] = df['RSI'].rolling(window=stoch_rsi_period).max()
    df['RSI_min'] = df['RSI'].rolling(window=stoch_rsi_period).min()

    # 분모가 0인 경우 처리
    df['STOCH_RSI'] = (df['RSI'] - df['RSI_min']) / (df['RSI_max'] - df['RSI_min'])
    df['STOCH_RSI'] = df['STOCH_RSI'].fillna(0)  # NaN 값은 0으로 처리하거나 다른 방법으로 처리 가능

    # 분모가 0인 경우 처리 (RSI_max == RSI_min인 경우)
    df['STOCH_RSI'] = df.apply(lambda row: 0 if row['RSI_max'] == row['RSI_min'] else row['STOCH_RSI'], axis=1)

    # UTC 시간을 한국시간으로 변환
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df['timestamp'] = df['timestamp'].dt.tz_convert('Asia/Seoul')

    return df

# 데이터 가져오기
market = "KRW-XRP"
df = get_upbit_ohlcv(market=market, interval="1", count=100)
df = df.sort_values(by='timestamp', ascending=True)

# STOCH RSI 계산
if df is not None:
    stoch_rsi_df = calculate_stoch_rsi(df)

    # 결과 출력
    print(stoch_rsi_df[['timestamp', 'RSI', 'STOCH_RSI']].all)
    plot_stoch_rsi(stoch_rsi_df)

import matplotlib
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# 사용할 폰트 설정 (운영체제별 적용)
plt.rcParams["font.family"] = "Arial"  # 기본 폰트 설정

# 1. 업비트 API에서 특정 코인의 시세 데이터 가져오기
def get_upbit_data(market="KRW-BTC", count=30):
    url = f"https://api.upbit.com/v1/candles/days"
    params = {"market": market, "count": count}
    response = requests.get(url, params=params)
    data = response.json()
    return pd.DataFrame(data)


# 2. VWMA(거래량 가중 이동 평균) 계산 함수
def volume_weighted_moving_average(data, period=5):
    price = data["trade_price"]  # 종가
    volume = data["candle_acc_trade_volume"]  # 거래량
    # 이동 평균 계산 (VWMA 공식 적용)
    vwma = (price * volume).rolling(window=period).sum() / volume.rolling(window=period).sum()
    return vwma


# 3. 데이터 가져오고 VWMA 계산
df = get_upbit_data("KRW-ADA", count=40)
df = df[::-1].reset_index(drop=True)
df["VWMA_5"] = volume_weighted_moving_average(df, period=5)
df["VWMA_20"] = volume_weighted_moving_average(df, period=20)
#20일 데이터 없는 부분 제외 VWMA 계산 완료 후
df = df.dropna(subset=["VWMA_20"])

# 4. 결과 출력
print(df[["candle_date_time_kst", "trade_price", "candle_acc_trade_volume", "VWMA_5", "VWMA_20"]].dropna())

# 5. 크로스 지점 계산
df["Cross"] = df["VWMA_5"] > df["VWMA_20"]  # True면 상승, False면 하락
df["Cross_Signal"] = df["Cross"].diff()  # 변할 때 크로스 발생

# 6. 마지막 크로스 지점 찾기
last_crossp = df[df["Cross_Signal"] != 0].iloc[-1] if not df[df["Cross_Signal"] != 0].empty else None
last_signal = " Long (Golden Cross)" if last_crossp is not None and last_crossp["Cross_Signal"] > 0 else "Short (Death Cross)"

# 6. 크로스 발생 시점 찾기
crosses = []
for i in range(1, len(df)):
    # 골든 크로스: 5일 VWMA가 20일 VWMA를 상향 돌파
    if df["VWMA_5"].iloc[i] > df["VWMA_20"].iloc[i] and df["VWMA_5"].iloc[i - 1] <= df["VWMA_20"].iloc[i - 1]:
        crosses.append(("golden", df["candle_date_time_kst"].iloc[i]))
    # 데드 크로스: 5일 VWMA가 20일 VWMA를 하향 돌파
    elif df["VWMA_5"].iloc[i] < df["VWMA_20"].iloc[i] and df["VWMA_5"].iloc[i - 1] >= df["VWMA_20"].iloc[i - 1]:
        crosses.append(("dead", df["candle_date_time_kst"].iloc[i]))

# 6. 마지막 크로스와 이전 크로스의 기간 차이 계산
if len(crosses) >= 2:
    last_cross = crosses[-1]
    previous_cross = crosses[-2]

    # 문자열을 datetime 형식으로 변환
    last_cross_date = pd.to_datetime(last_cross[1])
    previous_cross_date = pd.to_datetime(previous_cross[1])

    # 날짜 차이 계산
    days_diff = (last_cross_date - previous_cross_date).days
    print(f"최종 크로스 발생일: {last_cross_date}")
    print(f"이전 크로스 발생일: {previous_cross_date}")
    print(f"두 크로스 간의 기간 차이: {days_diff}일")
else:
    print("크로스 발생이 두 번 이상 없습니다.")
df["candle_date_time_kst"] = pd.to_datetime(df["candle_date_time_kst"])

# 7. 그래프 시각화
plt.figure(figsize=(14, 7))
sns.set_style("darkgrid")

# 종가 그래프
plt.plot(df["candle_date_time_kst"], df["trade_price"], label="Price", marker="o", linestyle="-", color="blue")

# 5일 VWMA 그래프
plt.plot(df["candle_date_time_kst"], df["VWMA_5"], label="VWMA (5-day)", marker="o", linestyle="--", color="red")

# 20일 VWMA 그래프
plt.plot(df["candle_date_time_kst"], df["VWMA_20"], label="VWMA (20-day)", marker="o", linestyle="--", color="green")

# 크로스 지점 표시
cross_points = df[df["Cross_Signal"] != 0]
plt.scatter(cross_points["candle_date_time_kst"], cross_points["VWMA_5"], color="black", label="Cross Point", zorder=3)

# 그래프 스타일
# X축 날짜 포맷 설정 (년-월-일 형식)
plt.xticks(df["candle_date_time_kst"], rotation=45, ha="right")
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xlabel("Date")
plt.ylabel("Price")
plt.title(f"VWMA (5-day & 20-day) Cross Analysis\n Direction: {last_signal}")
plt.legend()
plt.grid()

# 그래프 표시
plt.show()

# 최종 크로스 신호 출력
if last_cross is not None:
    print(f"📍 최종 크로스 날짜: {last_crossp['candle_date_time_kst']}")
    print(f"🚀 최종 방향: {last_signal}")
else:
    print("❌ 최근 50일 동안 크로스 발생 없음")

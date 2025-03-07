import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# 1. 업비트 API에서 시간별 데이터 가져오기 (1시간 봉)
def get_upbit_data(market="KRW-BTC", count=200):
    url = "https://api.upbit.com/v1/candles/minutes/60"
    params = {"market": market, "count": count}
    response = requests.get(url, params=params)
    df = pd.DataFrame(response.json())
    df = df[::-1].reset_index(drop=True)  # 역순 정렬
    return df

def filter_utc_data(df):
    df["candle_date_time_utc"] = pd.to_datetime(df["candle_date_time_utc"])
    df["candle_date_time_kst"] = pd.to_datetime(df["candle_date_time_kst"])
    df["hour"] = df["candle_date_time_utc"].dt.hour  # 시간 추출 (UTC 기준)
    df["khour"] = df["candle_date_time_kst"].dt.hour  # 시간 추출 (UTC 기준)
    return df

# 3. 데이터 가져오기
df = get_upbit_data("KRW-XRP", count=48)  # 최대 200개의 데이터 (약 8일치 데이터)

# 4. UTC 기준 하루 가격 변동 데이터
df_filtered = filter_utc_data(df)

# 5. 그래프 시각화 (일주일치 하루 가격 변동을 한 그래프에 표현)
unique_dates = df_filtered["candle_date_time_utc"].dt.date.unique()  # 유니크한 날짜 리스트

plt.figure(figsize=(14, 7))  # 그래프 크기 설정

# 6. X축을 0시부터 23시까지로 설정 (날짜 구분 없이)
plt.xlim(0,23)  # X축 범위: 0시부터 23시까지

# 7. 일주일치 하루 데이터 겹쳐서 그리기
colormap = plt.colormaps['tab10']  # 색상 팔레트 가져오기

# 8. 각 날짜별 데이터를 하나의 그래프에 그리기
for i, date in enumerate(unique_dates[:9]):  # 첫 7일치 데이터만 그리기
    daily_data = df_filtered[df_filtered["candle_date_time_utc"].dt.date == date]  # 해당 날짜의 데이터
    # 각 날짜의 '시간'을 기준으로 가격 변동 그리기
    plt.plot(daily_data["khour"].dt.hour, daily_data["trade_price"], label=f"Price on {date}",
             color=colormap(i))

# 그래프 스타일
plt.title("Price Fluctuation for a Week (UTC Time)")
plt.xlabel("Hour of the Day (UTC)")
plt.ylabel("Price")

# X축 시간 형식 설정 (0시부터 23시까지 시간만 표시)
plt.xticks(range(24))  # 0시부터 23시까지 표시

# 레전드 추가
plt.legend(title="Date", loc="upper left")

# 그리드 추가
plt.grid(True)

# 레이아웃 조정
plt.tight_layout()
plt.show()
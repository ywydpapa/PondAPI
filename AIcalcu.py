import requests
import pandas as pd
import numpy as np
import mplfinance as mpf


def get_upbit_candles(market, interval, unit, count):
    url = f"https://api.upbit.com/v1/candles/{interval}/{unit}"
    params = {"market": market, "count": count}
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df["candle_date_time_kst"] = pd.to_datetime(df["candle_date_time_kst"])
        df = df[["candle_date_time_kst", "opening_price", "high_price", "low_price", "trade_price",
                 "candle_acc_trade_volume"]]
        df.columns = ["date", "open", "high", "low", "close", "volume"]
        df.set_index("date", inplace=True)
        return df
    else:
        print("Error:", response.status_code, response.text)
        return None


def plot_candlestick_chart(df):
    mpf.plot(
        df,
        type="candle",
        style="charles",
        title="Upbit ETH/5min Candlestick Chart",
        ylabel="Price (KRW)",
        volume=True,  # 거래량 표시
        mav=(5, 10),  # 이동평균선 (5, 10)
    )


def calculate_rsi(df, period=14):
    if df.empty or 'close' not in df:
        print("⚠️ Warning: 데이터가 없습니다. RSI 계산을 건너뜁니다.")
        df['RSI'] = np.nan
        return df
    delta = df['close'].diff()
    # 🔹 상승분과 하락분 계산 (음수 방지)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    if len(gain) == 0 or len(loss) == 0:
        print("❌ Error: gain 또는 loss가 비어 있습니다.")
        df['RSI'] = np.nan
        return df

    avg_gain = pd.Series(gain).ewm(span=period, min_periods=1, adjust=False).mean()
    avg_loss = pd.Series(loss).ewm(span=period, min_periods=1, adjust=False).mean()
    avg_loss = avg_loss.replace(0, 1e-10)
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    rsi.name = 'RSI'
    rsif = rsi.to_frame()
    df = df.merge(rsif, left_index=True, right_index=True, how='left')
    return df


def plot_candlestick_with_cross(df, short_window, middle_window,long_window, coinn):
    # 이동평균선 계산
    df['short_MA'] = df['close'].rolling(window=short_window).mean()
    df['middle_MA'] = df['close'].rolling(window=middle_window).mean()
    df['long_MA'] = df['close'].rolling(window=long_window).mean()

    # 이동평균선 교차 지점 찾기
    df['signal'] = np.where(df['short_MA'] > df['long_MA'], 1, 0)
    df['cross'] = df['signal'].diff()

    # 골든크로스 & 데드크로스
    df['golden_cross'] = np.where(df['cross'] == 1, df['close'], np.nan)
    df['dead_cross'] = np.where(df['cross'] == -1, df['close'], np.nan)

    mc = mpf.make_marketcolors(
        up='red',  # 상승 캔들 색상
        down='blue',  # 하락 캔들 색상
        edge='inherit',
        wick='inherit',
        volume='inherit'
    )

    sty = mpf.make_mpf_style(marketcolors=mc)

    # 📈 캔들차트 그리기
    apds = [
        mpf.make_addplot(df['short_MA'], color='blue', width=1.5, label='Short MA'),
        mpf.make_addplot(df['middle_MA'], color='green', width=1.5, label='Middle MA'),
        mpf.make_addplot(df['long_MA'], color='red', width=1.5, label='Long MA'),
        mpf.make_addplot(df['golden_cross'], scatter=True, marker='^', color='green', markersize=100,
                         label='Golden Cross'),
        mpf.make_addplot(df['dead_cross'], scatter=True, marker='v', color='orange', markersize=100, label='Dead Cross'),
    ]
    titleset = f"{coinn} Candlestick Chart (MA Cross)"
    mpf.plot(df, type='candle', style=sty, title=titleset,
             ylabel="Price (KRW)", volume=True, addplot=apds, panel_ratios=(6, 2))

    return df[df['cross'] == 1], df[df['cross'] == -1]  # 골든/데드 크로스 값 반환

def getchart(coinn, unit, count):
    df = get_upbit_candles(coinn, "minutes", unit, count)
    df = df[::-1]
    golden_cross, dead_cross = plot_candlestick_with_cross(df, 3, 15, 30, coinn)
    print("🔹 골든크로스:\n", golden_cross[['close']])
    print("🔹 데드크로스:\n", dead_cross[['close']])

getchart("KRW-DOGE", 1, 180)
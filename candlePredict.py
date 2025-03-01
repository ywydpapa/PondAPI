import pyupbit
import pandas as pd
import numpy as np
import requests
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
import os


os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

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


def compute_rsi(data, period=14):
    delta = data.diff(1)  # 가격 변동 계산
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df = get_upbit_candles("KRW-XRP", "minutes", 3,60)
df = df[::-1]
df['rsi'] = compute_rsi(df['close'])
df.dropna(inplace=True)  # NaN 값 제거
df = df[['close', 'rsi']]

# Close와 RSI 각각 스케일러 적용
scaler_close = MinMaxScaler(feature_range=(0, 1))
scaler_rsi = MinMaxScaler(feature_range=(0, 1))

# Close 가격 정규화
df['close_scaled'] = scaler_close.fit_transform(df[['close']])

# RSI 정규화
df['rsi_scaled'] = scaler_rsi.fit_transform(df[['rsi']])

# 필요한 컬럼 선택
df_scaled = df[['close_scaled', 'rsi_scaled']].values
def create_sequences(data, seq_length=10, future_days=5):
    X, y = [], []
    for i in range(len(data) - seq_length - future_days):
        X.append(data[i:i+seq_length])  # 입력 (10일 데이터)
        y.append(data[i+seq_length:i+seq_length+future_days])  # 출력 (다음 5일 데이터)
    return np.array(X), np.array(y)

# 시퀀스 데이터 생성
seq_length = 10
future_days = 5
X, y = create_sequences(df_scaled, seq_length, future_days)

# 학습/테스트 데이터 분리 (80% 학습, 20% 테스트)
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

print(f"Train Shape: {X_train.shape}, Test Shape: {X_test.shape}")

# LSTM 모델 생성 (다음 5개 캔들의 Close 가격과 RSI 예측)
model = Sequential([
    LSTM(50, activation='relu', return_sequences=True, input_shape=(seq_length, 2)),
    LSTM(50, activation='relu', return_sequences=False),
    Dense(25),
    Dense(future_days * 2)  # 5개의 Close 가격과 5개의 RSI 예측 (5x2 = 10개 출력)
])

# 모델 컴파일
model.compile(optimizer='adam', loss='mean_squared_error')

# 모델 학습
model.fit(X_train, y_train.reshape(y_train.shape[0], -1), epochs=50, batch_size=16, validation_data=(X_test, y_test.reshape(y_test.shape[0], -1)))

# 예측 수행
predictions = model.predict(X_test)

# 3D → 2D 변환 (예측값과 실제값)
y_test_actual = y_test.reshape(-1, future_days, 2)
predictions_actual = predictions.reshape(-1, future_days, 2)

# 개별적으로 역변환 (Close & RSI)
y_test_close = scaler_close.inverse_transform(y_test_actual[:, :, 0])
y_test_rsi = scaler_rsi.inverse_transform(y_test_actual[:, :, 1].reshape(-1, 1))

predictions_close = scaler_close.inverse_transform(predictions_actual[:, :, 0])
predictions_rsi = scaler_rsi.inverse_transform(predictions_actual[:, :, 1].reshape(-1, 1))

# 마지막 예측된 5개 캔들 시각화 (Close 가격)
plt.figure(figsize=(10, 5))
plt.plot(y_test_close[-1], label="Actual Close Price", color='blue', marker='o')
plt.plot(predictions_close[-1], label="Predicted Close Price", color='red', linestyle='dashed', marker='o')
plt.legend()
plt.title("BTC/KRW LSTM Next 5 Candles Prediction (Close Price)")
plt.show()

# 마지막 10일 데이터를 이용해 다음 5개 캔들 예측
last_sequence = df_scaled[-seq_length:].reshape(1, seq_length, 2)
next_candles_scaled = model.predict(last_sequence)

# 예측된 값 (3D → 2D 변환)
next_candles_scaled = next_candles_scaled.reshape(future_days, 2)

# Close 가격과 RSI 각각 역변환
next_candles_close = scaler_close.inverse_transform(next_candles_scaled[:, 0].reshape(-1, 1))
next_candles_rsi = scaler_rsi.inverse_transform(next_candles_scaled[:, 1].reshape(-1, 1))

# 결과 출력
print("📈 Predicted Next 5 Candle Close Prices & RSI:")
for i in range(future_days):
    print(f"Day {i+1}: Close Price = {next_candles_close[i, 0]:,.0f} KRW, RSI = {next_candles_rsi[i, 0]:.2f}")
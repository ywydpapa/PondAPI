import requests
import pandas as pd

server_url = "https://api.upbit.com"

params = {
    "quote_currencies": "KRW"
}

res = requests.get(server_url + "/v1/ticker/all", params=params)
cpr = res.json()
df = pd.DataFrame(cpr)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
df['timestamp'] = df['timestamp'].dt.tz_convert('Asia/Seoul')

rises = df.query('change == "RISE"')
print(rises)
falls = df.query('change == "FALL"')
print(falls)

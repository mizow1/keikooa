import datetime

def split_at_10th_char(date_time_str):
  if len(date_time_str) < 10:
    raise ValueError(f"String must be at least 10 characters long: {date_time_str}")

  return date_time_str[:10], date_time_str[10:]

# 10文字目で分割し、日付と時間に分ける
for date_time_str in [
  "2024/05/2918:10",
  "2024/05/2512:01",
  "2024/05/2508:00",
  "2024/05/2412:13",
  "2024/05/2218:32",
  "2024/05/2217:00",
  "2024/05/2122:00",
  "2024/05/2022:00",
  "2024/05/2012:00",
  "2024/05/1812:01",
  "2024/05/0310:00",
]:
  date, time = split_at_10th_char(date_time_str)
  print(f"前半: {date}")
  print(f"後半: {time}")
  print("-----")
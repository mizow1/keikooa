# keiko lineoaの配信結果集計
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# 集計対象ページ
start_page = 1
end_page = 11


# ChromeDriverのパスを指定
# chrome_driver_path = '/path/to/chromedriver'

# ブラウザを起動
# service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # ヘッドレスモード（ブラウザを表示しない）
# driver = webdriver.Chrome(service=service, options=options)
driver = webdriver.Chrome()

wait = WebDriverWait(driver, 20)

# 指定のURLにアクセス
login_url = 'https://account.line.biz/login?redirectUri=https%3A%2F%2Fmanager.line.biz%2Faccount%2F%40246vizck'
driver.get(login_url)

# ①「LINEでログイン」ボタンを押す
line_login_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and .//i18n-message[@key="login.button.loginWithLine"]]'))
)
line_login_button.click()

# ② メールアドレスを入力
email_input = wait.until(EC.presence_of_element_located((By.NAME, "tid")))
email_input.send_keys("skunk0915@gmail.com")

# ③ パスワードを入力
password_input = wait.until(EC.presence_of_element_located((By.NAME, "tpasswd")))
password_input.send_keys("ane76urtmz")

# ④ ログインボタンを押す
login_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and contains(text(), "ログイン")]'))
)
login_button.click()


# ログイン後のページ遷移を待つ
wait = WebDriverWait(driver, 50)
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))

# データを収集する
data = []
base_url = 'https://manager.line.biz/account/@246vizck/insight/broadcast?page='

# 年月日と時間分割（10文字目で分割）
def split_at_10th_char(date_time_str):
  if len(date_time_str) < 10:
    raise ValueError(f"String must be at least 10 characters long: {date_time_str}")

  return date_time_str[:10], date_time_str[10:]


for page in range(start_page, end_page):
    url = base_url + str(page)
    driver.get(url)
    
    # tbodyの内容を取得
    # tbody = driver.find_element(By.CSS_SELECTOR, 'tbody[data-v-c0033a1e=""]')
    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table.table-hover.table-layout-fixed.my-4')))
    tbody = table.find_element(By.TAG_NAME, 'tbody')

    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        cols_text = [col.text.replace('\n', '').replace(',', '') for col in cols]
        date, time_str = split_at_10th_char(cols_text[0])
        cols_text[0] = f"{date} {time_str}"
        data.append(cols_text)
    
    time.sleep(2)  # 各ページのロードを待つために一時停止

# DataFrameにデータを保存し、CSVファイルに出力
df = pd.DataFrame(data)
df.to_csv('line_insight_data.csv', index=False, header=False)

# ブラウザを閉じる
driver.quit()

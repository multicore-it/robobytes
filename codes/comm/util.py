import pandas as pd
import datetime
import time
import requests

#타임스템프에서 초 추출
def get_time_ss(mili_time):
    mili_time = float(mili_time)
    KST = datetime.timezone(datetime.timedelta(hours=9))
    dt = datetime.datetime.fromtimestamp(mili_time, tz=KST)
    timeline = str(dt.strftime('%S'))
    return timeline

#타임스템프에서 분 추출
def get_time_mm(mili_time):
    mili_time = float(mili_time)
    KST = datetime.timezone(datetime.timedelta(hours=9))
    dt = datetime.datetime.fromtimestamp(mili_time, tz=KST)
    timeline = str(dt.strftime('%M'))
    return timeline

#타임스템프에서 시간 추출
def get_time_hhmmss(mili_time):
    mili_time = float(mili_time)
    KST = datetime.timezone(datetime.timedelta(hours=9))
    dt = datetime.datetime.fromtimestamp(mili_time, tz=KST)
    timeline = str(dt.strftime('%D %H:%M:%S'))
    return timeline

#로그 기록
def log_info(message):
    print("{}".format(message))

#1분 데이터 가져오기
def get_web_1m_data(base_candle_url):
    for i in range(0, 3):  # 오류가 난다면 최대 3번까지 반복하면서 데이터를 가져온다.
        try:
            webpage = requests.get(base_candle_url, timeout=3)
            df_candle_temp = pd.read_json(webpage.content)
            break
        except:
            print("*pd.read_json(webpage.content) error !!! ")
        time.sleep(1) #오류 발생하면 1초 후 다시 시도

    rename_columns = {0: 't', 1: 'o', 2: 'h', 3: 'l', 4: 'c', 5: 'v'}
    df = df_candle_temp[[0, 1, 2, 3, 4, 5]].rename(columns=rename_columns)

    return df

#오픈건수 계산
def check_open_cnt(check_data, amt_list):
    idx = 1
    for data in amt_list:
        if round(check_data,0) == round(data,0):
            return idx
        idx = idx + 1
    return idx

#단계별 구매 수량
def get_open_amt_list(open_amt_unit, open_cnt_limit, increace_rate):
    open_amt = 0
    open_amt_list = [0.0]
    for idx in range(0, open_cnt_limit):
        temp_amt = open_amt_unit + open_amt * increace_rate
        open_amt = round(open_amt + temp_amt, 4)
        open_amt_list.append(open_amt)
    return open_amt_list

#손실 최소화 실현 금액
def get_max_loss(close, open_amt_unit, open_cnt_limit, increace_rate, max_loss_rate):
    open_amt = 0
    open_price = 0
    for idx in range(0, open_cnt_limit):
        temp_amt = open_amt_unit + open_amt * increace_rate
        open_price = round(open_price + close * temp_amt, 4)
        open_amt = round(open_amt + temp_amt, 4)
    return round(open_price/open_amt * max_loss_rate, 4)
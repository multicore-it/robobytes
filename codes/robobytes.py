import time
import comm.config as conf
import comm.trade as trade
import comm.util as util
import comm.calc_indicators as calc
from binance_f import RequestClient

######(1) 변수 초기화 ######
g_api_key = conf.G_API_KEY       # binance API key
g_secret_key = conf.G_SECRET_KEY # binance secret key
coin_name = 'XRPUSDT'
request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
base_candle_url = "https://www.binance.com/fapi/v1/klines?symbol={}&interval=1m".format(coin_name)

#파라미터 설정
revenue_rate = 0.011  #익절 비율
max_loss_rate = 0.18  #손절 비율
increace_rate = 0.25  #포지션 증가 비율
open_cnt_limit = 7    #최대 오픈 건수
open_amt_unit = 9     #최소 오픈 수량
open_amt_list = []    #단계별 주문수량
open_amt_list = util.get_open_amt_list(open_amt_unit, open_cnt_limit, increace_rate)
max_loss = 0          #손절 가격(stop loss 주문시 계산)

trade_flag = 1  #0:trade not yet, 1:trade done
vwap = 0        #이전분 vwap
close = 0       #이전분 종가

open_long_amt = 0           #롱 포지션 오픈 수량
open_short_amt = 0          #숏 포지션 오픈 수량
process_sleep_time = 0.2    #대시시간
long_order_id = ""          #오픈 롱 포지션 아이디
short_order_id = ""         #오픈 숏 포지션 아이디
profit_long_id = ""         #오픈 롱 이익 실현 주문 아이디
profit_short_id = ""        #오픈 숏 이익 실현 주문 아이디
stop_long_id = ""           #오픈 롱 손실 최소화 주문 아이디
stop_short_id = ""          #오픈 숏 손실 최소화 주문 아이디
profit_long_amt = 0         #롱 이익 실현 주문 수량
profit_short_amt = 0        #숏 이익 실현 주문 수량
stop_long_amt = 0           #롱 손실 최소화 주문 수량
stop_short_amt = 0          #숏 손실 최소화 주문 수량

util.log_info("*********** start trading ***********")
######(2) 주문 초기화(미체결 주문 전체 취소)
message = trade.cancel_pending_order(request_client, coin_name, "long")
if message != 'good':
    util.log_info("+[{}]long cancel_pending_order error msg:{}".
                  format(util.get_time_hhmmss(time.time()), message))
message = trade.cancel_pending_order(request_client, coin_name, "short")
if message != 'good':
    util.log_info("+[{}]short cancel_pending_order error msg:{}".
                  format(util.get_time_hhmmss(time.time()), message))

while True:
    check_ss = util.get_time_ss(time.time()) #초단위 체크
    ######(3) 분데이터 가져오기, 분데이터는 6초후 생성 start ######
    if check_ss in ('06','07','08','09','10'):
        #데이터 가져오기
        df = util.get_web_1m_data(base_candle_url)
        df['vwap'] = calc.get_vwap(df['h'],df['l'],df['c'],df['v'], 14)
        df_one = df.iloc[df.shape[0]-1:,] #마지막 한 건 가져오기
        vwap = df_one['vwap'].values[0]
        close = df_one['c'].values[0]
        trade_flag = 0

        ######(4) 30분 마다 take_profie, stop_loss 주문 취소 ######
        check_mm = util.get_time_mm(time.time()) #분단위 체크
        if check_mm in ('00', '30'): #30분 마다 take_profie, stop_loss 주문 취소
            #take profit 주문이 실행됐을 때 stop loss 주문은 예전 주문이 그대로 있는 경우 발생
            message = trade.cancel_pending_order(request_client, coin_name, "long")
            if message != 'good':
                util.log_info("+[{}]long cancel_pending_order error msg:{}".
                              format(util.get_time_hhmmss(time.time()), message))
            message = trade.cancel_pending_order(request_client, coin_name, "short")
            if message != 'good':
                util.log_info("+[{}]short cancel_pending_order error msg:{}".
                              format(util.get_time_hhmmss(time.time()), message))
            util.log_info("+[{}] cancel_pending_order (stop loss & take profit) msg:{}".
                          format(util.get_time_hhmmss(time.time()), message))
    ###### 분데이터 가져오기, 분데이터는 6초후 생성 end ######

    ######(5) position open start ######
    if trade_flag == 0 and check_ss in ('58','59','00','01'):
        trade_flag = 1
        ###(5)-1 cancel before timestep order ###
        if long_order_id != "":
            status, message = trade.ask_order_status(request_client, coin_name, long_order_id)
            if message != 'good':
                util.log_info("+[{}]cancel before timestep-long ask_order_status error msg:{}".
                              format(util.get_time_hhmmss(time.time()), message))
                continue
            if status == "NEW": #open long order 미체결, 주문 취소
                result, message = trade.trade_cancle(request_client, coin_name, long_order_id)
                if message != 'good':
                    util.log_info("+[{}]cancel before timestep-long trade_cancle error msg:{}".
                                  format(util.get_time_hhmmss(time.time()), message))
                    continue
                time.sleep(process_sleep_time)
        if short_order_id != "":
            status, message = trade.ask_order_status(request_client, coin_name, short_order_id)
            if message != 'good':
                util.log_info("+[{}]cancel before timestep-short ask_order_status error msg:{}".
                              format(util.get_time_hhmmss(time.time()), message))
                continue
            if status == "NEW": #open short order 미체결, 주문 취소
                result, message = trade.trade_cancle(request_client, coin_name, short_order_id)
                if message != 'good':
                    util.log_info("+[{}]cancel before timestep-short trade_cancle error msg:{}".
                                  format(util.get_time_hhmmss(time.time()), message))
                    continue
                time.sleep(process_sleep_time)
        ### cancel before timestep order ###

        ###(5)-2 long position open start ###
        amt, entry_price, message = trade.get_position_amt(request_client, coin_name, 'LONG')
        if message != 'good':
            util.log_info("+[{}]long position open-get_position_amt error msg:{}".
                          format(util.get_time_hhmmss(time.time()), message))
            continue
        time.sleep(process_sleep_time)
        open_long_cnt = util.check_open_cnt(amt, open_amt_list)
        # print("***try open long amt:{} open_long_cnt:{} close:{} vwap:{}".
        #       format(amt, open_long_cnt, close, vwap))
        if open_long_cnt <= open_cnt_limit and close < vwap:
            open_long_amt = open_amt_unit + amt * increace_rate
            # open_long_amt = amt + temp_amt
            # 호가조회
            order_bid, order_ask, message = trade.ask_order_book(request_client, coin_name)
            if message != 'good':
                util.log_info("+[{}]long position open-ask_order_book error msg:{}".
                              format(util.get_time_hhmmss(time.time()), message))
                continue
            # 거래 단위 조정
            trade_price = "{:0.0{}f}".format(order_ask, 4) #소수점 첫째자리
            trade_amt = "{:0.0{}f}".format(open_long_amt, 1)  #소수점 넷째자리
            # open long position
            long_order_id, message = trade.trade_buy_long(request_client, coin_name, trade_amt, trade_price)
            if message != 'good':
                util.log_info("+[{}]long open position-trade_buy_long error msg:{}".
                              format(util.get_time_hhmmss(time.time()), message))
                continue
            trading_msg = "*[{}]long open position id:{} v:{} c:{} p:{} a:{} m:{}".format(
                util.get_time_hhmmss(time.time()), long_order_id, vwap, close, trade_price, trade_amt, message)
            util.log_info(trading_msg)
            time.sleep(process_sleep_time)
        ### long position open end ###

        ###(5)-3 short position open start ###
        amt, entry_price, message = trade.get_position_amt(request_client, coin_name, 'SHORT')
        if message != 'good':
            util.log_info("+[{}]short open position-get_position_amt error msg:{}".
                          format(util.get_time_hhmmss(time.time()), message))
            continue
        time.sleep(process_sleep_time)
        open_short_cnt = util.check_open_cnt(amt, open_amt_list)

        if open_short_cnt <= open_cnt_limit and close > vwap:
            open_short_amt = open_amt_unit + amt * increace_rate
            # open_short_amt = amt + temp_amt
            # 호가조회
            order_bid, order_ask, message = trade.ask_order_book(request_client, coin_name)
            if message != 'good':
                util.log_info("+[{}]short open position-ask_order_book error msg:{}".
                              format(util.get_time_hhmmss(time.time()), message))
                continue
            # 거래 단위 조정
            trade_price = "{:0.0{}f}".format(order_bid, 4)  # 소수점 첫째자리
            trade_amt = "{:0.0{}f}".format(open_short_amt, 1)  # 소수점 넷째자리
            # open short position
            short_order_id, message = trade.trade_buy_short(request_client, coin_name, trade_amt, trade_price)
            trading_msg = "*[{}]short open position id:{} v:{} c:{} p:{} a:{} m:{}".format(
                util.get_time_hhmmss(time.time()), short_order_id, vwap, close, trade_price, trade_amt, message)
            util.log_info(trading_msg)
            time.sleep(process_sleep_time)
        ### short position open end ###
    ###### position open end ######

    ######(6) take profit start #####
    ###(6)-1 prepare take profit
    # take profit 주문이 체결되었다면 profit amt를 0으로 만들어서 새로운 take profit 주문을 준비한다.
    if profit_long_id != "":
        status, message = trade.ask_order_status(request_client, coin_name, profit_long_id)
        if message != 'good':
            util.log_info("+[{}]prepare take profit-long ask_order_status error msg:{}".
                          format(util.get_time_hhmmss(time.time()), message))
            continue
        if status != "NEW": #주문 체결
            profit_long_id = ""
            profit_long_amt = 0
    if profit_short_id != "":
        status, message = trade.ask_order_status(request_client, coin_name, profit_short_id)
        if message != 'good':
            util.log_info("+[{}]prepare take profit-short ask_order_status error msg:{}".
                          format(util.get_time_hhmmss(time.time()), message))
            continue
        if status != "NEW": #주문 체결
            profit_short_id = ""
            profit_short_amt = 0

    ###(6)-2 LONG Take Profit start ###
    amt, entry_price, message = trade.get_position_amt(request_client, coin_name, 'long')
    if message != 'good':
        util.log_info("+[{}]long take profit-get_position_amt error msg:{}".
                      format(util.get_time_hhmmss(time.time()), message))
        continue
    diff_amt = amt - profit_long_amt
    if diff_amt > 0:
        # 이전 주문 취소, 모든 주문을 취소하고 전체를 다시 주문한다.
        if profit_long_id != "":
            result, message = trade.trade_cancle(request_client, coin_name, profit_long_id)
            if message == 'good':
                util.log_info("+[{}]long take profit-trade_cancle error id:{} msg:{}".
                              format(util.get_time_hhmmss(time.time()), profit_long_id, message))
                continue
            time.sleep(process_sleep_time)
        order_bid, order_ask, message = trade.ask_order_book(request_client, coin_name)
        profit_price = "{:0.0{}f}".format((entry_price + entry_price * revenue_rate),4)
        stop_price = "{:0.0{}f}".format((order_ask + 0.0002), 4)
        trade_amt = "{:0.0{}f}".format(amt, 1)
        order_id_profit, message = trade.trade_buy_long_take_profit(
            request_client, coin_name, trade_amt, profit_price, stop_price)
        if message == 'good':
            profit_long_id = order_id_profit
            profit_long_amt = amt
        util.log_info(
            "*[{}]long take profit id:{} amt:{} stop_price:{} profit_price:{} msg:{}".format(
                util.get_time_hhmmss(time.time()), order_id_profit, trade_amt,
                stop_price, profit_price, message)
        )
        time.sleep(process_sleep_time)
    ### LONG Take Profit end ###

    ###(6)-3 SHORT Take Profit start ###
    amt, entry_price, message = trade.get_position_amt(request_client, coin_name, 'short')
    diff_amt = amt - profit_short_amt
    if diff_amt > 0:
        # 이전 주문 취소, 모든 주문을 취소하고 전체를 다시 주문한다.
        if profit_short_id != "":
            result, message = trade.trade_cancle(request_client, coin_name, profit_short_id)
            if message != 'good':
                util.log_info("+[{}]short take profit-trade_cancle error id:{} msg:{}".
                              format(util.get_time_hhmmss(time.time()), profit_short_id, message))
                continue
            time.sleep(process_sleep_time)
        order_bid, order_ask, message = trade.ask_order_book(request_client, coin_name)
        if message != 'good':
            util.log_info("+[{}]short take profit-ask_order_book error msg:{}".
                          format(util.get_time_hhmmss(time.time()), message))
            continue
        profit_price = "{:0.0{}f}".format((entry_price - entry_price * revenue_rate),4)
        stop_price = "{:0.0{}f}".format((order_bid - 0.0002), 4)
        trade_amt = "{:0.0{}f}".format(amt, 1)
        order_id_profit, message = trade.trade_buy_short_take_profit(
            request_client, coin_name, trade_amt, profit_price, stop_price)
        if message == 'good':
            profit_short_id = order_id_profit
            profit_short_amt = amt
        util.log_info(
            "*[{}]short take profit id:{} amt:{} stop_price:{} profit_price:{} msg:{}".format(
                util.get_time_hhmmss(time.time()), profit_short_id, trade_amt,
                stop_price, profit_price, message)
        )
        time.sleep(process_sleep_time)
    ### SHORT Take Profit end ###
    ###### take profit end #####

    ######(7) stop loss start #####
    ###(7)-1 prepare stop loss
    # stop loss 주문이 체결되었다면 stop loss amt를 0으로 만들어서 새로운 stop loss 주문을 준비한다.
    if stop_long_id != "":
        status, message = trade.ask_order_status(request_client, coin_name, stop_long_id)
        if message != 'good':
            util.log_info("+[{}]prepare stop loss-long ask_order_status error msg:{}".
                          format(util.get_time_hhmmss(time.time()), message))
            continue
        if status != "NEW": #주문 체결
            stop_long_amt = 0
            stop_long_id = ""
    if stop_short_id != "":
        status, message = trade.ask_order_status(request_client, coin_name, stop_short_id)
        if message != 'good':
            util.log_info("+[{}]prepare stop loss-short ask_order_status error msg:{}".
                          format(util.get_time_hhmmss(time.time()), message))
            continue
        if status != "NEW": #주문 체결
            stop_short_amt = 0
            stop_short_id = ""

    ###(7)-2 LONG stop loss start ###
    amt, entry_price, trade_message = trade.get_position_amt(request_client, coin_name, 'long')
    diff_amt = amt - stop_long_amt
    if diff_amt > 0:
        # 이전 주문 취소, 모든 주문을 취소하고 전체를 다시 주문한다.
        if stop_long_id != "":
            result, message = trade.trade_cancle(request_client, coin_name, stop_long_id)
            if message != 'good':
                util.log_info("+[{}]long stop loss-trade_cancle error msg:{}".
                              format(util.get_time_hhmmss(time.time()), message))
                continue
            stop_long_id = ""
            time.sleep(process_sleep_time)
        max_loss = util.get_max_loss(entry_price, open_amt_unit, open_cnt_limit, increace_rate, max_loss_rate)
        stop_price = "{:0.0{}f}".format((entry_price - max_loss),4)
        trade_amt = "{:0.0{}f}".format(amt, 1)
        order_id_stop, message = trade.trade_stop_market(
            request_client, coin_name, stop_price, trade_amt, "long")
        if message == 'good':
            stop_long_id = order_id_stop
            stop_long_amt = amt
        util.log_info(
            "*[{}]long stop loss id:{} amt:{} max_loss:{} stop_price:{} msg:{}".format(
                util.get_time_hhmmss(time.time()), order_id_stop, trade_amt, max_loss,
                stop_price, message)
        )
        time.sleep(process_sleep_time)
    ### LONG stop loss end ###

    ###(7)-3 SHORT stop loss start ###
    amt, entry_price, trade_message = trade.get_position_amt(request_client, coin_name, 'short')
    diff_amt = amt - stop_short_amt
    if diff_amt > 0:
        # 이전 주문 취소, 모든 주문을 취소하고 전체를 다시 주문한다.
        if stop_short_id != "":
            result, message = trade.trade_cancle(request_client, coin_name, stop_short_id)
            if message != 'good':
                util.log_info("+[{}]short stop loss-trade_cancle error msg:{}".
                              format(util.get_time_hhmmss(time.time()), message))
                continue
            time.sleep(process_sleep_time)
        max_loss = util.get_max_loss(entry_price, open_amt_unit, open_cnt_limit, increace_rate, max_loss_rate)
        stop_price = "{:0.0{}f}".format((entry_price + max_loss), 4)
        trade_amt = "{:0.0{}f}".format(amt, 1)
        order_id_stop, message = trade.trade_stop_market(
            request_client, coin_name, stop_price, trade_amt, "short")
        if message == 'good':
            stop_short_id = order_id_stop
            stop_short_amt = amt
        util.log_info(
            "*[{}]short stop loss id:{} amt:{} max_loss:{}  stop_price:{} msg:{}".format(
                util.get_time_hhmmss(time.time()), order_id_stop, trade_amt, max_loss,
                stop_price, message)
        )
        time.sleep(process_sleep_time)
    ### SHORT stop loss end ###
    ###### stop loss end #####

    time.sleep(1) #2초후 다시 시도

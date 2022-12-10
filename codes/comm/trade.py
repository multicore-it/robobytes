from binance_f.exception.binanceapiexception import *
from binance_f.model.constant import *
import sys

#레버리지 설정
def set_leverage(request_client, coin_name, leverage):
    result = -1
    try:
        result = request_client.change_initial_leverage(symbol=coin_name, leverage=leverage)
    except:
        result = -1
    return result

#매수: LONG POSITION
def trade_buy_long(request_client, coin_name, param_buy_coin_amt, trade_price):
    order_id = "error"
    trade_message = "good"
    try:
        result = request_client.post_order(
            symbol=coin_name,
            side=OrderSide.BUY,
            ordertype=OrderType.LIMIT,
            quantity=param_buy_coin_amt,
            price=trade_price,
            timeInForce="GTC",
            positionSide="LONG"
        )
        order_id = result.orderId
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
    except:
        trade_message = "{}".format(sys.exc_info())

    return str(order_id), trade_message

#매수: LONG POSITION
def trade_buy_long(request_client, coin_name, param_buy_coin_amt, trade_price):
    order_id = "error"
    trade_message = "good"
    try:
        result = request_client.post_order(
            symbol=coin_name,
            side=OrderSide.BUY,
            ordertype=OrderType.LIMIT,
            quantity=param_buy_coin_amt,
            price=trade_price,
            timeInForce="GTC",
            positionSide="LONG"
        )
        order_id = result.orderId
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
    except:
        trade_message = "{}".format(sys.exc_info())

    return str(order_id), trade_message

#매수: LONG POSITION : TAKE PROFIT
def trade_buy_long_take_profit(request_client, coin_name, param_buy_coin_amt, profit_price, stop_price):
    order_id = "error"
    trade_message = "good"
    try:
        result = request_client.post_order(
            symbol=coin_name,
            side=OrderSide.SELL,
            ordertype=OrderType.TAKE_PROFIT,
            quantity=param_buy_coin_amt,
            price=profit_price,
            stopPrice=stop_price,
            timeInForce="GTC",
            positionSide="LONG"
        )
        order_id = result.orderId
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
    except:
        trade_message = "{}".format(sys.exc_info())

    return str(order_id), trade_message

# 매수: SHORT POSITION
def trade_buy_short(request_client, coin_name, param_buy_coin_amt, trade_price):
    order_id = "error"
    trade_message = "good"
    try:
        result = request_client.post_order(
            symbol=coin_name,
            side=OrderSide.SELL,
            ordertype=OrderType.LIMIT,
            quantity=param_buy_coin_amt,
            price=trade_price,
            timeInForce="GTC",
            positionSide="SHORT"
        )
        order_id = result.orderId
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
    except:
        trade_message = "{}".format(sys.exc_info())

    return str(order_id), trade_message

# 매수: SHORT POSITION : TAKE PROFIT
def trade_buy_short_take_profit(request_client, coin_name, param_buy_coin_amt, profit_price, stop_price):
    order_id = "error"
    trade_message = "good"
    try:
        result = request_client.post_order(
            symbol=coin_name,
            side=OrderSide.BUY,
            ordertype=OrderType.TAKE_PROFIT,
            quantity=param_buy_coin_amt,
            price=profit_price,
            stopPrice=stop_price,
            timeInForce="GTC",
            positionSide="SHORT"
        )
        order_id = result.orderId
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
    except:
        trade_message = "{}".format(sys.exc_info())

    return str(order_id), trade_message

#포지션 종료: LONG POSITION
def trade_close_long(request_client, coin_name, param_buy_coin_amt, order_type, trade_price=0):
    order_id = "error"
    trade_message = "good"

    try:
        if order_type == 'market':
            result = request_client.post_order(
                symbol=coin_name,
                side=OrderSide.SELL,
                ordertype=OrderType.MARKET,
                quantity=param_buy_coin_amt,
                positionSide="LONG"
            )
            order_id = result.orderId
        elif order_type == 'limit':
            result = request_client.post_order(
                symbol=coin_name,
                side=OrderSide.SELL,
                ordertype=OrderType.LIMIT,
                quantity=param_buy_coin_amt,
                price=trade_price,
                timeInForce="GTC",
                positionSide="LONG"
            )
            order_id = result.orderId
        else:
            trade_message = "invalid order_type(market or limit)"
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
    except:
        trade_message = "{}".format(sys.exc_info())
    return str(order_id), trade_message

#포지션 종료: SHORT POSITION
def trade_close_short(request_client, coin_name, param_buy_coin_amt, order_type, trade_price=0):
    order_id = "error"
    trade_message = "good"
    try:
        if order_type == 'market':
            result = request_client.post_order(
                symbol=coin_name,
                side=OrderSide.BUY,
                ordertype=OrderType.MARKET,
                quantity=param_buy_coin_amt,
                positionSide="SHORT"
            )
            order_id = result.orderId
        elif order_type == 'limit':
            result = request_client.post_order(
                symbol=coin_name,
                side=OrderSide.BUY,
                ordertype=OrderType.LIMIT,
                quantity=param_buy_coin_amt,
                price=trade_price,
                timeInForce="GTC",
                positionSide="SHORT"
            )
            order_id = result.orderId
        else:
            trade_message = "invalid order_type(market or limit)"
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
    except:
        trade_message = "{}".format(sys.exc_info())
    return str(order_id), trade_message

#손절
def trade_stop_market(request_client, coin_name, stop_price, param_buy_coin_amt, bid_position):
    order_id = "error"
    trade_message = "good"
    try:
        if bid_position == 'long':
            result = request_client.post_order(
                symbol=coin_name,
                side=OrderSide.SELL,
                ordertype=OrderType.STOP_MARKET,
                stopPrice= str(stop_price),  # 현재가 보다 높은 가격
                quantity=str(param_buy_coin_amt),
                positionSide="LONG"
            )
            order_id = result.orderId
        if bid_position == 'short':
            result = request_client.post_order(
                symbol=coin_name,
                side=OrderSide.BUY,
                ordertype=OrderType.STOP_MARKET,
                stopPrice=str(stop_price),  # 현재가 보다 높은 가격
                quantity=str(param_buy_coin_amt),
                positionSide="SHORT"
            )
            order_id = result.orderId
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
    except:
        trade_message = "{}".format(sys.exc_info())
    return str(order_id), trade_message

#주문 취소
def trade_cancle(request_client, coin_name, order_id):
    result = -1
    trade_message = 'good'
    try:
        result = request_client.cancel_order(symbol=coin_name, orderId="{}".format(order_id))
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
        result = -1
    except:
        trade_message = "{}".format(sys.exc_info())
        result = -1

    return result, trade_message #CANCELED: 정상처리

#전체 미체결 주문 취소
def cancel_all_orders(request_client, coin_name):
    trade_message = "good"
    try:
        result = request_client.cancel_all_orders(symbol=coin_name)
        status = result.code
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
        status = -1
    except:
        status = -1
        trade_message = sys.exc_info()[0]
    return status, trade_message  # code:200


#주문 상태 조회
def ask_order_status(request_client, coin_name, order_id):
    status = -1
    trade_message = "good"
    try:
        result = request_client.get_order(symbol=coin_name, orderId="{}".format(order_id))
        status = result.status
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
        status = -1
    except:
        trade_message = "{}".format(sys.exc_info())
        status = -1

    return status, trade_message #NEW:대기, FILLED:체결

def ask_order_book(request_client, coin_name):
    bid = -1
    ask = -1
    trade_message = 'good'
    try:
        result = request_client.get_order_book(symbol = coin_name, limit = 10)
        bid = result.bids[0].price #매수
        ask = result.asks[0].price #매도
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
    except:
        trade_message = "{}".format(sys.exc_info())

    return float(bid), float(ask), trade_message

#계좌내역 확인
def ask_balance(request_client, coin_name):
    result = 0
    trade_message = "good"
    try:
        balances = request_client.get_balance()
        for i in balances:
            result = result + i.balance
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
        result = -1
    except:
        trade_message = "{}".format(sys.exc_info())

    return result, trade_message  # NEW:대기, FILLED:체결

#미체결 주문 전체 취소
def cancel_pending_order(request_client, coin_name, position):
    results = request_client.get_open_orders(symbol=coin_name)
    trade_message = 'good'
    for result in results:
        if result.status == 'NEW' and result.positionSide == position.upper():
            try:
                trade_cancle(request_client, coin_name, result.orderId)
            except BinanceApiException as e:
                trade_message = "{} {}".format(e.error_code, e.error_message)
                break
            except:
                trade_message = sys.exc_info()[0]
                break
    return trade_message  # NEW:대기, FILLED:체결

#오픈된 포지션 정보 조회
def get_position_amt(request_client, coin_name, position):
    amt = 0.0
    tmp_entry_price = 0.0
    trade_message = 'good'
    cnt = 0
    try:
        results = request_client.get_position()
        for result in results:
            if result.symbol == coin_name.upper() and result.positionSide == position.upper():
                cnt = cnt + 1
                tmp_entry_price = tmp_entry_price + float(result.entryPrice)
                amt = amt + float(result.positionAmt)
    except BinanceApiException as e:
        trade_message = "{} {}".format(e.error_code, e.error_message)
    except:
        trade_message = sys.exc_info()[0]
    entry_price = (tmp_entry_price / cnt) if cnt > 0 else 0
    return abs(amt), abs(entry_price), trade_message  # NEW:대기, FILLED:체결
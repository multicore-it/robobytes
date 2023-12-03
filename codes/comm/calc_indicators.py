from ta.trend import SMAIndicator
from ta.trend import WMAIndicator
from ta.trend import EMAIndicator
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.momentum import StochRSIIndicator
from ta.volatility import BollingerBands
from ta.volume import VolumeWeightedAveragePrice

# 단순 이동평균
def get_sma(close, period):
    df_sma = SMAIndicator(close, window=period).sma_indicator()
    return df_sma

# 가중 이동평균
def get_wma(close, period):
    df_wma = WMAIndicator(close, window=period).wma()
    return df_wma

# 지수 이동평균
def get_ema(close, period):
    df_wma = EMAIndicator(close, window=period).ema_indicator()
    return df_wma

# MACD
def get_macd(close, period_slow, period_fast, period_sign):
    macd = MACD(close, window_slow=period_slow, window_fast=period_fast, window_sign=period_sign)
    df_macd = macd.macd()
    df_macd_s = macd.macd_signal()
    df_macd_d = macd.macd_diff()
    return df_macd, df_macd_s, df_macd_d

# RSI
def get_rsi(close, period):
    df_rsi = RSIIndicator(close, window=period).rsi()
    return df_rsi

# StochRSI
def get_stochRSI(close, period, period_s1, period_s2):
    stochRSI = StochRSIIndicator(close, window=period, smooth1=period_s1, smooth2=period_s2)
    df_srsi = stochRSI.stochrsi()
    df_srsik = stochRSI.stochrsi_k()
    df_srsid = stochRSI.stochrsi_d()
    return df_srsi, df_srsik, df_srsid

# Bollinger Bands
def get_bb(close, period, period_dev):
    bb = BollingerBands(close, window=period, window_dev=period_dev)
    df_bh = bb.bollinger_hband()  # high band
    df_bhi = bb.bollinger_hband_indicator()  # high band 보다 가격이 높으면 1, 아니면 0
    df_bl = bb.bollinger_lband()  # low band
    df_bli = bb.bollinger_lband_indicator()  # low band 보다 가격이 낮으면 1, 아니면 0
    df_bm = bb.bollinger_mavg()  # middle band
    df_bw = bb.bollinger_wband()  # band width
    return df_bh, df_bhi, df_bl, df_bli, df_bm, df_bw

#VWAP
def get_vwap(high, low, close, vol, period):
    vwap = VolumeWeightedAveragePrice(high=high, low=low, close=close, volume=vol, window=period)
    df_vwap = vwap.volume_weighted_average_price()
    return df_vwap
import os
import pyupbit
import pandas as pd
import json
from application.service import my_indicator as my_indicator
from dotenv import load_dotenv


load_dotenv()
upbit = pyupbit.Upbit(os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY"))


def get_current_status():
    """
    현재 상태를 가져오는 함수입니다.
    주문 도서, 현재 시간, BTC 잔액, KRW 잔액, BTC 평균 구매 가격을 포함한 현재 상태를 반환합니다.
    """
    orderbook = pyupbit.get_orderbook(ticker="KRW-BTC")
    current_time = orderbook['timestamp']
    btc_balance = 0
    krw_balance = 0
    btc_avg_buy_price = 0
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == "BTC":
            btc_balance = b['balance']
            btc_avg_buy_price = b['avg_buy_price']
        if b['currency'] == "KRW":
            krw_balance = b['balance']

    current_status = {'current_time': current_time, 'orderbook': orderbook, 'btc_balance': btc_balance,
                      'krw_balance': krw_balance, 'btc_avg_buy_price': btc_avg_buy_price}
    return json.dumps(current_status)


def buy_coin(ticker, min_balance, amount):
    """
    코인을 구매하는 함수입니다.
    최소 잔액이 충분한 경우에만 구매를 시도합니다.
    """
    print("Attempting to buy BTC...")
    try:
        krw = upbit.get_balance("KRW")
        if krw >= min_balance:
            # result = upbit.buy_market_order("KRW-BTC", krw*0.9995)
            result = upbit.buy_market_order(ticker, amount)
            print("Buy order successful:", result)
    except Exception as e:
        print(f"Failed to execute buy order: {e}")


def sell_all_coin(balance_ticker, order_ticker):
    """
    모든 코인을 판매하는 함수입니다.
    현재 가격과 코인 잔액을 곱한 값이 5000 이상인 경우에만 판매를 시도합니다.
    """
    print("Attempting to sell BTC...")
    try:
        coin = upbit.get_balance(balance_ticker)
        current_price = pyupbit.get_orderbook(ticker=order_ticker)['orderbook_units'][0]["ask_price"]
        if current_price * coin > 5000:
            result = upbit.sell_market_order(order_ticker, coin)
            print("Sell order successful:", result)
    except Exception as e:
        print(f"Failed to execute sell order: {e}")


def get_balance(ticker):
    """
    주어진 티커에 대한 잔액을 가져오는 함수입니다.
    """
    return upbit.get_balance(ticker)


def buy_market_order(ticker, amount):
    """
    시장 가격으로 주어진 티커를 구매하는 함수입니다.
    """
    return upbit.buy_market_order(ticker, amount)


def fetch_and_prepare_data():
    """
    데이터를 가져오고 준비하는 함수입니다.
    한 달간의 일일 데이터와 최근 24시간의 시간당 데이터를 가져와서 각 데이터에 지표를 추가합니다.
    """
    sma_lengths = [10, 21]
    ema_lengths = [10, 21]
    rsi_lengths = [9, 14]
    stoch_lengths = [10 + 2]
    all_lengths = sma_lengths + ema_lengths + rsi_lengths + stoch_lengths
    offset_length = max(all_lengths)
    # print(f"Offset length: {offset_length}")

    # Fetch data
    df_hourly = pyupbit.get_ohlcv("KRW-BTC", interval="minute60", count=24+offset_length)
    df_15min = pyupbit.get_ohlcv("KRW-BTC", "minute15", count=96+offset_length)

    # Define a helper function to add indicators
    def add_indicators(df):
        # Moving Averages
        df['SMA_10'] = my_indicator.get_sma(df, 10)
        df['EMA_10'] = my_indicator.get_ema(df, 10)
        df['SMA_21'] = my_indicator.get_sma(df, 21)
        df['EMA_21'] = my_indicator.get_ema(df, 21)

        # RSI
        df['RSI_9'] = my_indicator.get_rsi(df, 9)
        df['RSI_14'] = my_indicator.get_rsi(df, 14)

        # Stochastic Oscillator
        df = my_indicator.join_stoch(df, 10, 3, 2)
        # df = my_indicator.join_stoch(df, 14, 3, 3)

        # MACD
        df = my_indicator.get_applied_macd(df, 9, 21, 7)
        # df = my_indicator.get_applied_macd(df, 12, 26, 9)

        # Bollinger Bands
        df = my_indicator.get_applied_bollinger_bands(df, 10)
        # df = my_indicator.get_applied_bollinger_bands(df, 20)

        return df

    # Add indicators to both dataframes
    # 한달간 일봉과 24시간간 1시간봉 데이터를 가져와서 각각의 데이터에 지표를 추가합니다.
    df_hourly = add_indicators(df_hourly).iloc[offset_length:]
    df_15min = add_indicators(df_15min).iloc[offset_length:]

    combined_df = pd.concat([df_hourly, df_15min], keys=['hourly', '15min'])
    # df_print(combined_df)
    combined_data = combined_df.to_json(orient='split')

    # make combined data as string and print length
    print(len(combined_data))

    return json.dumps(combined_data)


def has_coin(ticker):
    """
    주어진 티커에 대한 코인을 가지고 있는지 여부를 반환하는 함수입니다.
    """
    return get_balance(ticker) > 0


def df_print(df):
    """
    데이터프레임을 출력하는 함수입니다.
    """
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(df)

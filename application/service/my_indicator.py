import pandas_ta as ta


def get_sma(df, length):
    return ta.sma(df['close'], length)


def get_ema(df, length):
    return ta.ema(df['close'], length)


def get_rsi(df, length):
    return ta.rsi(df['close'], length)


def get_stoch(df, k, d, smooth_k):
    return ta.stoch(df['high'], df['low'], df['close'], k, d, smooth_k)


def get_applied_macd(df, fast_span, slow_span, signal_span):
    ema_fast = df['close'].ewm(span=fast_span, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow_span, adjust=False).mean()
    df['MACD'] = ema_fast - ema_slow
    df['Signal_Line'] = df['MACD'].ewm(span=signal_span, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
    return df


def get_applied_bollinger_bands(df, window):
    df['Middle_Band'] = df['close'].rolling(window=window).mean()
    # Calculate the standard deviation of closing prices over the last 20 days
    std_dev = df['close'].rolling(window=window).std()
    # Calculate the upper band (Middle Band + 2 * Standard Deviation)
    df['Upper_Band'] = df['Middle_Band'] + (std_dev * 2)
    # Calculate the lower band (Middle Band - 2 * Standard Deviation)
    df['Lower_Band'] = df['Middle_Band'] - (std_dev * 2)
    return df


def join_stoch(df, k, d, smooth_k):
    return df.join(get_stoch(df, k, d, smooth_k))

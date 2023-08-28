import pandas as pd
import numpy as np
import talib
import utils.util

if __name__ == '__main__':
    file = "./恒指主连_HSImain_K_5M.csv"
    pd_reader = pd.read_csv(file)

    m = {}
    l = pd_reader['Time_key'].values.tolist()
    close_price = pd_reader['Close'].values.tolist()
    open_price = pd_reader['Open'].values.tolist()
    high_price = pd_reader['High'].values.tolist()
    low_price = pd_reader['Low'].values.tolist()

    upper, middle, lower = talib.BBANDS(np.array(close_price), timeperiod=20, matype=talib.MA_Type.EMA)

    for i in range(3, len(close_price)):
        if utils.util.trade_hk_time(l[i]):
            if close_price[i - 2] < open_price[i - 2] and close_price[i - 2] < lower[i - 2] and close_price[i - 1] < \
                    open_price[i - 1] and close_price[i - 1] < lower[i - 1] and close_price[i] < lower[i]:
                print(l[i])

import os
from datetime import datetime, timedelta

import pandas as pd
import backtrader as bt

from testStratagy import VerifyStratagy
import config


def loadDataFrameFromPklFile(file_name, folder_abs_path=None):
    folder_abs_path = folder_abs_path if folder_abs_path else PandasConfig.APP_DATA_PATH()
    filepath = os.path.join(folder_abs_path, file_name)
    return pd.read_feather(filepath)


if __name__ == '__main__':
    cerebro = bt.Cerebro(stdstats=False)

    cerebro.addstrategy(VerifyStratagy)

    cerebro.adddata(bt.feeds.PandasData(
        dataname=loadDataFrameFromPklFile(f'{config.TradePair}.pkl', folder_abs_path='./data'),
        fromdate=datetime(2023, 1, 1, 0, 0, 0),
        todate=datetime(2023, 9, 1, 0, 0, 0),
        datetime='open_time',
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=-1
    ), name='BTCUSDT')

    cerebro.broker.setcommission(commission=0.0002)
    cerebro.addsizer(bt.sizers.FixedSize, stake=1)
    cerebro.broker.setcash(100000)

    cerebro.addobserver(bt.observers.Trades)
    cerebro.addobserver(bt.observers.BuySell)
    cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addobserver(bt.observers.Value)
    cerebro.addobserver(bt.observers.TimeReturn)

    print(cerebro.broker.getvalue())
    cerebro.run()
    print(cerebro.broker.getvalue())

    cerebro.plot(style='candle')
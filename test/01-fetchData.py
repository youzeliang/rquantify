# move this demo file to your application root path.
#  eg. from python_library.utils.appUtils import AppUtils

import os, time, itertools
from datetime import datetime, timedelta
import logging
import pandas as pd

import ccxt

import config

INTERVAL_MAP = {
    86400:   '1d',
}

"""
获取期货k线OHLCV数据
Parameters:
    self                    myExchange(Public)
    underlying              - str           - underlying
    base_asset              - str           - base_asset
    start_time              - datetime      - 查询起始时间
    interval                - ETimeConstant - 间隔
    sample_size             - int           - 样本容量
Returns:
    exchange                - str               - binance
    open_time               - datetime64[ns]    - k线开始时间(UTC时间)
    interval                - int               - base_asset
    start_time              - datetime          - 间隔
    open                    - float             - open
    high                    - float             - high
    low                     - float             - low
    close                   - float             - close
    volume                  - float             - volume
Raises:
    (ccxt)
"""
def getFutureOHLCVSample(exchange, trade_pair: str, start_time: datetime, interval: int, sample_size: int):

    future_kline_sample = pd.DataFrame()
    while future_kline_sample.shape[0] < sample_size:
        REQ_LIMIT = 1500
        req_start_time = start_time + timedelta(weeks=0, days=0, hours=0, minutes=0, seconds=interval * future_kline_sample.shape[0], microseconds=0, milliseconds=0)
        if req_start_time > datetime.now(): break
        params = {
            'pair': 		    trade_pair,
            'contractType': 	'PERPETUAL',
            'interval':         INTERVAL_MAP[interval],
            'startTime':        int(time.mktime(req_start_time.timetuple())) * 1000,
            'limit':            min(REQ_LIMIT, sample_size - future_kline_sample.shape[0])
        }
        data = exchange.fapiPublicGetContinuousKlines(params=params)
        data = pd.DataFrame(data, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_volume', 'taker_buy_quote_asset_volume', 'ignore'])

        data['interval'] = interval
        data['open_time'] = pd.to_datetime(data['open_time'], unit='ms')
        data[['open']] = data[['open']].astype(float)
        data[['high']] = data[['high']].astype(float)
        data[['low']] = data[['low']].astype(float)
        data[['close']] = data[['close']].astype(float)
        data[['volume']] = data[['volume']].astype(float)

        data = data[['open_time', 'interval', 'open', 'high', 'low', 'close', 'volume']]

        # 合并统计数据
        future_kline_sample_lines = future_kline_sample.shape[0]
        future_kline_sample = pd.concat(objs=[future_kline_sample, data])
        future_kline_sample.drop_duplicates(['open_time'], inplace=True)
        # assert future_kline_sample_lines < future_kline_sample.shape[0]

    # future_kline_sample['exchange'] = type(self).EXCHANGE_NAME
    return future_kline_sample



def appendDataFrameToLocalFile(file_name, append_data, folder_abs_path=None, sort_values=[], drop_duplicates=[]):
    folder_abs_path = folder_abs_path if folder_abs_path else PandasConfig.APP_DATA_PATH()
    if not os.path.exists(folder_abs_path): os.mkdir(folder_abs_path)
    filepath = os.path.join(folder_abs_path, file_name)
    # logger.debug(f"Start append DataFrame to file [{filepath}]. append_data.shape=[{append_data.shape}], sort_values=[{sort_values}], drop_duplicates=[{drop_duplicates}]...")

    if not os.path.exists(filepath):
        append_data.to_feather(filepath)
        # logger.debug(f"just created file [{filepath}]...")
    else:
        data = pd.read_feather(filepath)
        data = pd.concat([data, append_data])
        append_data.reset_index(inplace=True)
        if len(drop_duplicates) > 0:
            data.drop_duplicates(drop_duplicates, inplace=True)
        if len(sort_values) > 0:
            data.sort_values(sort_values, inplace=True)
        data.reset_index(drop=True, inplace=True)
        data.to_feather(filepath)
    #     logger.debug(f"[{filepath}] already exist, update data done, file_data.shape=[{data.shape}]...")

    # logger.info(f"append DataFrame to file [{filepath}] Done. sort_values=[{sort_values}], drop_duplicates=[{drop_duplicates}], append_data.shape=[{append_data.shape}]")



if __name__ == '__main__':

    klines = getFutureOHLCVSample(exchange=ccxt.binance(), trade_pair=config.TradePair, start_time=config.DataStartTime, interval=config.Interval, sample_size=400)

    appendDataFrameToLocalFile(f'{config.TradePair}.pkl', klines, drop_duplicates=['open_time'], sort_values=['open_time'], folder_abs_path='./data')

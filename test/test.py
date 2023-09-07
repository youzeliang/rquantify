
import os, time, itertools
from datetime import datetime, timedelta
import logging
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.min_rows', None)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('expand_frame_repr', False)


import config

def find_peaks(arr, time_list):
    """
    寻找波峰
    :param arr:
    :param time_list:
    :return:
    """
    peaks = []
    t = []
    if len(arr) == 0:
        return [], []
    min_value = min(arr)
    last_value = min(arr)

    for i in range(2, len(arr) - 2):
        if arr[i] > arr[i - 1] and arr[i] > arr[i + 1] and arr[i] > arr[i + 2] and arr[i] > arr[i - 2] and arr[i] >= last_value:

            if len(peaks) >= 2 and i - peaks[-1] <= 3:
                peaks[-1] = i
                continue
            peaks.append(i)
            last_value = arr[i]
            t.append(time_list[i])
        if arr[i] == min_value:
            last_value = min(arr)
            t = []
            peaks = []

    return [arr[i] for i in peaks], t


def find_valleys(arr, time_list):
        """
        寻找波谷
        :param arr:
        :param time_list:
        :return:
        """
        valleys = []
        t = []
        if len(arr) == 0:
            return [], []
        max_value = max(arr)
        last_value = max(arr)

        for i in range(2, len(arr) - 2):
            if arr[i] < arr[i - 1] and arr[i] < arr[i + 1] and arr[i] < arr[i + 2] and arr[i] < arr[i - 2] and arr[i] <= last_value:

                if len(valleys) >= 2 and i - valleys[-1] <= 3:
                    valleys[-1] = i
                    continue
                valleys.append(i)
                last_value = arr[i]
                t.append(time_list[i])
            if arr[i] == max_value:
                last_value = max(arr)
                t = []
                valleys = []

        return [arr[i] for i in valleys], t

def loadDataFrameFromPklFile(file_name, folder_abs_path=None):
    folder_abs_path = folder_abs_path if folder_abs_path else PandasConfig.APP_DATA_PATH()
    filepath = os.path.join(folder_abs_path, file_name)
    return pd.read_feather(filepath)


data = loadDataFrameFromPklFile(f'{config.TradePair}.pkl', folder_abs_path='./data')


print(data)



# result = pd.DataFrame(find_peaks(data['close'], data['open_time']))
result = pd.DataFrame(find_valleys(data['close'], data['open_time']))
print(result)
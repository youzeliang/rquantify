
import backtrader





class VerifyStratagy(backtrader.Strategy):
    params = dict(  pivot_left = 2,
                    pivot_right = 2,
                    PVs_len_threshold = 3,
                    PLOT_SWITCH = False,
                    RECORD_TO_FILE = False)

    def log(self, txt, dt=None, log_level='DEBUG', doprint=True):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        if doprint:
            print(f'[{dt.isoformat()}]: {txt}')

    def __init__(self):
        self.peakarr_sliding_window = []
        self.valleyarr_sliding_window = []

    def find_valleys(self):
        valleys = []
        if len(self.valleyarr_sliding_window) == 0:
            return 0
        max_value = max(self.valleyarr_sliding_window)
        last_value = max(self.valleyarr_sliding_window)

        for i in range(self.params.pivot_left, len(self.valleyarr_sliding_window) - self.params.pivot_right):
            valley_hit = True
            for e in range(1, self.params.pivot_left + 1):
                if self.valleyarr_sliding_window[i] > self.valleyarr_sliding_window[i-e]: valley_hit = False
            for e in range(1, self.params.pivot_right + 1):
                if self.valleyarr_sliding_window[i] > self.valleyarr_sliding_window[i+e]: valley_hit = False
            if self.valleyarr_sliding_window[i] > last_value: valley_hit = False

            if valley_hit:
                if len(valleys) >= 2 and i - valleys[-1] <= 3:
                    valleys[-1] = i
                    continue
                valleys.append(i)
                last_value = self.valleyarr_sliding_window[i]
            if self.valleyarr_sliding_window[i] == max_value:
                last_value = max(self.valleyarr_sliding_window)
                valleys = []
        return len(valleys)


    def find_peaks(self):
        peaks = []
        if len(self.peakarr_sliding_window) == 0:
            return 0
        min_value = min(self.peakarr_sliding_window)
        last_value = min(self.peakarr_sliding_window)

        for i in range(self.params.pivot_left, len(self.peakarr_sliding_window) - self.params.pivot_right):
            peak_hit = True
            for e in range(1, self.params.pivot_left + 1):
                if self.peakarr_sliding_window[i] < self.peakarr_sliding_window[i-e]: peak_hit = False
            for e in range(1, self.params.pivot_right + 1):
                if self.peakarr_sliding_window[i] < self.peakarr_sliding_window[i+e]: peak_hit = False
            if self.peakarr_sliding_window[i] < last_value: peak_hit = False

            if peak_hit:
                if len(peaks) >= 2 and i - peaks[-1] <= 3:
                    peaks[-1] = i
                    continue
                peaks.append(i)
                last_value = self.peakarr_sliding_window[i]
            if self.peakarr_sliding_window[i] == min_value:
                last_value = min(self.peakarr_sliding_window)
                peaks = []

        return len(peaks)


    def next(self):

        data = self.getdatabyname('BTCUSDT')
        self.peakarr_sliding_window.append(data.close[0])
        self.valleyarr_sliding_window.append(data.close[0])

        self.log(f'{type(self).__name__}.nextBar: Time:[{data.datetime.datetime(0)}], Current position: {self.getposition().size}; dataclose[0]=[{data.close[0]}], len(self.peakarr_sliding_window)=[{len(self.peakarr_sliding_window)}], len(self.valleyarr_sliding_window)=[{len(self.valleyarr_sliding_window)}].', log_level='INFO')


        if self.find_peaks() >= self.params.PVs_len_threshold:
            self.sell()
            self.peakarr_sliding_window = []
            self.log(f'Peak found at Time:[{data.datetime.datetime(0)}].')


        if self.find_valleys() >= self.params.PVs_len_threshold:
            self.buy()
            self.valleyarr_sliding_window = []
            self.log(f'Valley found at Time:[{data.datetime.datetime(0)}].')


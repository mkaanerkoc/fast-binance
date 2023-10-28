import pandas as pd


class FileInfo:
    def prepare_df(self, df):
        raise NotImplementedError('prepare_df() method should be implemented in derived classes.')

class PriceKlinesFile(FileInfo):
    columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
               'quote_volume', 'count', 'taker_buy_volume', 'taker_buy_quote_volume', 'ignore']

    type_mapping = {'open_time':int, 'open':float, 'high':float, 'low':float, 'close':float,
                    'volume':float, 'quote_volume':float, 'taker_buy_volume':float }

    def __init__(self, market, symbol, period, date, span='daily'):
        self.binance = BinanceKlinesFile(market, symbol, period, date, span)

    def prepare_df(self, df:pd.DataFrame):
        try:
            df.columns = self.columns
            df = df.astype(self.type_mapping)
            df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
            df.set_index('open_time', inplace=True)
        except Exception as e:
            print(e)
        finally:
            return df


class FuturesUsdtMetricsFile(FileInfo):
    def __init__(self, symbol, date):
        self.binance = BinanceMetricsFile(symbol, date)

    def prepare_df(self, df):
        try:
            #TODO
            pass
        except Exception as e:
            print(e)
        finally:
            return df

class PremiumIndexKlinesFile(FileInfo):
    columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
               'quote_volume', 'count', 'taker_buy_volume', 'taker_buy_quote_volume', 'ignore']

    type_mapping = {'open_time':int, 'open':float, 'high':float, 'low':float, 'close':float }

    def __init__(self, symbol, date, span, period):
        # Can we find span by looking at date?
        self.binance = BinancePremiumIndexFile(symbol, date, span, period)
    
    def prepare_df(self, df:pd.DataFrame):
        try:
            df.columns = self.columns
            df = df.astype(self.type_mapping)
            df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
            df.set_index('open_time', inplace=True)
            df.drop(columns=['close_time','volume','taker_buy_volume', 
                             'quote_volume', 'taker_buy_quote_volume', 
                             'ignore'], inplace=True)
        except Exception as e:
            print(e)
        finally:
            return df

class MarkPriceKlines:
    pass

class BinanceKlinesFile:
    def __init__(self, market, symbol, period, date, span):
        self.market = market
        self.symbol = symbol
        self.period = period
        self.date = date
        self.span = span

    @property
    def path(self):
        if self.market == 'futures':
            return f"https://data.binance.vision/data/futures/um/"\
               f"{self.span}/klines/{self.symbol}/{self.period}/{self.symbol}-{self.period}-{self.date}.zip"
        elif self.market == 'spot':
            return f"https://data.binance.vision/data/spot/"\
                f"{self.span}/klines/{self.symbol}/{self.period}/{self.symbol}-{self.period}-{self.date}.zip"

class BinanceMetricsFile:
    def __init__(self, symbol, date):
        self.symbol = symbol
        self.date = date
        self._base_url = 'https://data.binance.vision/data/futures/um'
        
    @property
    def path(self):
        return  f'{self._base_url}/daily/metrics/{self.symbol}/{self.symbol}-metrics-{self.date}.zip'


class BinancePremiumIndexFile:
    def __init__(self, symbol, date, span, period):
        self.symbol = symbol
        self.date = date
        self.period = period
        self._span = span
        self._base_url = 'https://data.binance.vision/data/futures/um'
    

    @property
    def path(self):
        '''
        https://data.binance.vision/data/futures/um/monthly/premiumIndexKlines/TRBUSDT/1m/TRBUSDT-1m-2023-09.zip
        '''
        return f'{self._base_url}/{self._span}/premiumIndexKlines/' \
            f'{self.symbol}/{self.period}/{self.symbol}-{self.period}-{self.date}.zip'
        

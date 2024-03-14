import pandas as pd


class AbstractFile:
    _base_url = 'https://data.binance.vision/data'
    @property
    def source(self):
        raise NotImplementedError('source() method should be implemented in derived classes.')

    def prepare_df(self, df):
        raise NotImplementedError('prepare_df() method should be implemented in derived classes.')


class KlinesFile(AbstractFile):
    columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
               'quote_volume', 'count', 'taker_buy_volume', 'taker_buy_quote_volume', 'ignore']
     
    def __init__(self, market, symbol, period, date, span):
        self.market = 'spot' if market == 'spot' else 'futures/um'
        self.symbol = symbol
        self.period = period
        self.date = date
        self.span = span
        self.name = f'{self.symbol}-{self.period}-{self.date}'

class MetricsFile:
    def __init__(self, symbol, date):
        self.symbol = symbol
        self.date = date
        self._base_url = 'https://data.binance.vision/data/futures/um'
        
    @property
    def source(self):
        return  f'{self._base_url}/daily/metrics/{self.symbol}/{self.symbol}-metrics-{self.date}.zip'


class PriceKlinesFile(KlinesFile):
    type_mapping = {'open_time':int, 'open':float, 'high':float, 'low':float, 'close':float,
                    'volume':float, 'quote_volume':float, 'taker_buy_volume':float }

    def __init__(self, market, symbol, period, date, span='daily'):
        super().__init__(market, symbol, period, date, span)

    @property
    def source(self):
        '''
        https://data.binance.vision/data/futures/um/daily/klines/ACHUSDT/15m/ACHUSDT-15m-2024-02-07.zip
        '''
        return f'{self._base_url}/{self.market}/{self.span}/klines/{self.symbol}/{self.period}/{self.name}.zip'

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

class FuturesUsdtMetricsFile(AbstractFile):
    def __init__(self, symbol, date):
        self.binance = MetricsFile(symbol, date)

    def prepare_df(self, df):
        try:
            #TODO
            pass
        except Exception as e:
            print(e)
        finally:
            return df

class PremiumIndexKlinesFile(KlinesFile):
    type_mapping = {'open_time':int, 'open':float, 'high':float, 'low':float, 'close':float }

    def __init__(self, symbol, period, date, span):
        # Can we find span by looking at date?
        super().__init__('futures', symbol, period, date, span)
        
    
    def prepare_df(self, df:pd.DataFrame):
        try:
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
        
    @property
    def source(self):
        '''
        https://data.binance.vision/data/futures/um/monthly/premiumIndexKlines/TRBUSDT/1m/TRBUSDT-1m-2023-09.zip
        '''
        return f'{self._base_url}/futures/um/{self.span}/premiumIndexKlines/' \
            f'{self.symbol}/{self.period}/{self.symbol}-{self.period}-{self.date}.zip'

class MarkPriceKlines:
    # TODO
    pass


class PremiumIndexFile:
    def __init__(self, symbol, date, span, period):
        self.symbol = symbol
        self.date = date
        self.period = period
        self._span = span
        self._base_url = 'https://data.binance.vision/data/futures/um'
    
    @property
    def source(self):
        '''
        https://data.binance.vision/data/futures/um/monthly/premiumIndexKlines/TRBUSDT/1m/TRBUSDT-1m-2023-09.zip
        '''
        return f'{self._base_url}/{self._span}/premiumIndexKlines/' \
            f'{self.symbol}/{self.period}/{self.symbol}-{self.period}-{self.date}.zip'

class AggregatedTradesFile(AbstractFile):
    def __init__(self, symbol, date, span, market):
        self.symbol = symbol
        self.date = date
        self.span = span
        self.market = 'spot' if market == 'spot' else 'futures/um'
        self.name = f'{self.symbol}-aggTrades-{self.date}' # ACAUSDT-aggTrades-2024-02-07
        self.columns = ['aggTradeID', 'price', 'quantity', 'ftId', 'ltId', 'time', 'is_buyer_maker', 'ig']  if market == 'spot' \
                        else ['aggTradeID', 'price', 'quantity', 'ftId', 'ltId', 'time', 'is_buyer_maker']

    @property
    def source(self):
        '''
        https://data.binance.vision/data/spot/daily/aggTrades/ACAUSDT/ACAUSDT-aggTrades-2024-02-07.zip
        https://data.binance.vision/data/futures/um/daily/aggTrades/ACAUSDT/ACAUSDT-aggTrades-2024-02-07.zip
        '''
        return f'{self._base_url}/{self.market}/{self.span}/aggTrades/{self.symbol}/{self.name}.zip'
    
    @property
    def local(self):
        pass

    def prepare_df(self, df):
        print('IM HERE 1', self.columns)
        df.columns = self.columns
        df = df.astype({"time":int})
        print('IM HERE 1b')
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        print('IM HERE 2')
        df = df.drop(columns=['ftId', 'ltId', 'ig'])
        df = df.set_index(df['time']).sort_index()
        print('IM HERE 3')
        return df


class FileInfo:
    pass

class KlinesFile(FileInfo):
    def __init__(self, market, symbol, period, date, span='daily'):
        self.binance = BinanceKlinesFile(market, symbol, period, date, span)

class FuturesUsdtMetricsFile(FileInfo):
    def __init__(self, symbol, date):
        self.binance = BinanceMetricsFile(symbol, date)

class PriceKlines:
    pass

class PremiumIndexKlines:
    pass

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
        self.futures_base_url = 'https://data.binance.vision/data/futures/um'
        
    @property
    def path(self):
        return  f'{self.futures_base_url}/daily/metrics/{self.symbol}/{self.symbol}-metrics-{self.date}.zip'


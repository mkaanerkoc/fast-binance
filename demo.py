import pandas as pd
from itertools import product


from fast_binance import (
    OnlinePriceFetcher,
    OfflineFileFetcher,
    AggregatedTradesFile,
    FuturesUsdtMetricsFile,
    PremiumIndexKlinesFile,
    PriceKlinesFile
)

def main():
    pf = OnlinePriceFetcher('spot')
    res = pf.download(['SEIUSDT', 'FTTUSDT', 'BTCUSDT'], 
                        interval='1h', 
                        start_str='2023-07-01',
                        end_str='2023-08-01' )
    print(res)

def archieve_data():
    ofl = OfflineFileFetcher()
    dates = pd.date_range('2023-05-10', '2023-06-20', freq='1D')
    files = [FuturesUsdtMetricsFile(symbol, str(date.date())) 
             for symbol, date in product(['TRBUSDT', 'LTCUSDT'], dates)]
    res = ofl.download(files)
    print(res)

def analyze_premium_index():
    ofl = OfflineFileFetcher()
    symbol = 'SANDUSDT'
    dates = pd.date_range('2020-01-01', '2023-11-01', freq='1M')
    
    months = [f'{date.year}-{date.month:02d}' for date in dates]
    
    files = [PremiumIndexKlinesFile(symbol, month, 'monthly', '1m') 
             for symbol, month in product([symbol], months)]
    
    res = ofl.download(files)
    df = pd.concat(list(filter(lambda x: isinstance(x, pd.DataFrame), res)))
    df.to_csv(f'{symbol}_premium_index.csv')

    files = [PriceKlinesFile('futures', symbol, '1m', month, 'monthly') 
             for symbol, month in product([symbol], months)]
    
    res = ofl.download(files)
    df = pd.concat(list(filter(lambda x: isinstance(x, pd.DataFrame), res)))
    df.to_csv(f'{symbol}_fut_klines.csv')


def analyze_premium_index_daily():
    ofl = OfflineFileFetcher()
    symbol = 'LOOMUSDT'
    
    days = pd.date_range('2023-09-01', '2023-11-01', freq='1D')
    
    files = [PremiumIndexKlinesFile(symbol, '1m', str(day.date()), 'daily') 
             for symbol, day in product([symbol], days)]
    
    res = ofl.download(files)
    df = pd.concat(list(filter(lambda x: isinstance(x, pd.DataFrame), res)))
    df.to_csv(f'{symbol}_premium_index.csv')


    files = [PriceKlinesFile('futures', symbol, '1m', str(day.date()), 'daily') 
             for symbol, day in product([symbol], days)]
    
    res = ofl.download(files)
    df = pd.concat(list(filter(lambda x: isinstance(x, pd.DataFrame), res)))
    df.to_csv(f'{symbol}_fut_klines.csv')

def download_agg_trades():
    ofl = OfflineFileFetcher()
    symbol = 'LOOMUSDT'
    
    days = pd.date_range('2023-09-01', '2023-11-01', freq='1D')

    files = [AggregatedTradesFile(symbol, str(day.date()), 'daily', 'spot') 
             for symbol, day in product([symbol], days)]
    
    res = ofl.download(files)
    df = pd.concat(list(filter(lambda x: isinstance(x, pd.DataFrame), res)))
    df.to_csv(f'{symbol}_agg_trades.csv')

def analyze_premium_index_daily_multiple_symbol():
    ofl = OfflineFileFetcher()
    symbol = 'LOOMUSDT'
    
    days = pd.date_range('2023-09-01', '2023-11-01', freq='1D')
    
    files = [PremiumIndexKlinesFile(symbol, str(day.date()), 'daily', '1m') 
             for symbol, day in product([symbol], days)]
    
    res = ofl.download(files)
    df = pd.concat(list(filter(lambda x: isinstance(x, pd.DataFrame), res)))
    df.to_csv(f'{symbol}_premium_index.csv')

    files = [PriceKlinesFile('futures', symbol, '1m', str(day.date()), 'daily') 
             for symbol, day in product([symbol], days)]
    
    res = ofl.download(files)
    df = pd.concat(list(filter(lambda x: isinstance(x, pd.DataFrame), res)))
    df.to_csv(f'{symbol}_fut_klines.csv')


if __name__ == '__main__':
    download_agg_trades()
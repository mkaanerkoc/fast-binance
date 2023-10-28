import pandas as pd
from itertools import product


from fast_binance import (
    OnlinePriceFetcher,
    OfflineFileFetcher,
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


if __name__ == '__main__':
    archieve_data()
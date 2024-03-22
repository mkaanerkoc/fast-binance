__version__ = "1.1.2"

from fast_binance.online_fetcher import (
  OnlinePriceFetcher,
  OpenInterestFetcher,
  MultiplexFetcher,
)

from fast_binance.offline_fetcher import OfflineFileFetcher

from fast_binance.archieve_files import(
    PriceKlinesFile,
    FuturesUsdtMetricsFile,
    MarkPriceKlines,
    PremiumIndexKlinesFile,
    AggregatedTradesFile
)
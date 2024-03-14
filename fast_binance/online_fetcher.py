import asyncio

from binance import AsyncClient, Client

import pandas as pd

from fast_binance.utils import chunked_iterable

DEFAULT_WORKER_COUNT = 30

CANDLE_COLUMNS  = ['open_time', 'open', 'high', 'low', 'close', 'volume', 
                    'close_time', 'quote_volume', 'count', 
                    'taker_buy_volume', 'taker_buy_quote_volume', 'ignore']

OI_STATS_COLUMNS = ['symbol', 'sumOpenInterest', 'sumOpenInterestValue', 'timestamp']

  
def convert_price_data_types(raw_prices:pd.DataFrame, convert_types=True):
    """ converts non-processed price data into useful DataFrame format.

    Args:
        raw_prices (pd.DataFrame): non-indexed, no types defined DataFrame

    Returns:
        pd.DataFrame: DateTimeIndex'ed, type defined DataFrame
    """
    raw_prices.columns = CANDLE_COLUMNS
    raw_prices['open_time'] = pd.to_datetime(raw_prices['open_time'], unit='ms')
    # raw_prices = raw_prices.drop(['ignore', 'close_time', 'taker_buy_volume'], axis=1)
    if convert_types:
        raw_prices = raw_prices.astype({'open': 'float64', 
                                        'close': 'float64', 
                                        'high':'float64', 
                                        'low':'float64',
                                        'volume':'float64',
                                        'count':'int64',
                                        'quote_volume':'float64',
                                        'taker_buy_volume':'float64',
                                        'taker_buy_quote_volume':'float64'})
    raw_prices = raw_prices.set_index('open_time')
    return raw_prices


def convert_oi_data(oi_data:pd.DataFrame, convert_types=True):
    oi_data.columns = OI_STATS_COLUMNS
    if convert_types:
        oi_data = oi_data.astype({
            'timestamp': 'int64', 
            'sumOpenInterest': 'float64', 
            'sumOpenInterestValue':'float64',
    })
    oi_data['timestamp'] = pd.to_datetime(oi_data['timestamp'], unit='ms')
    oi_data = oi_data.set_index('timestamp')
    return oi_data


class HistoricalFundingRate:
    def __init__(self):
        self._client = Client()

    def download(self):
        response = self._client.futures_funding_rate(limit=1000)
        funding_rate = pd.DataFrame(response)
        funding_rate['fundingTime'] = pd.to_datetime(funding_rate['fundingTime'], unit='ms')
        funding_rate = funding_rate.set_index('symbol')
        return funding_rate
    

class MarkPrice:
    def __init__(self):
        self._client = Client()

    def download(self):
        response = self._client.futures_mark_price()
        mark_price = pd.DataFrame(response)
        mark_price['nextFundingTime'] = pd.to_datetime(mark_price['nextFundingTime'], unit='ms')
        mark_price['time'] = pd.to_datetime(mark_price['time'], unit='ms')
        mark_price = mark_price.set_index('symbol')
        return mark_price

class PriceResult:
    def __init__(self, symbols, interval, start, end):
        pass
    
    def save(self):
        pass

    def load(self):
        pass

class MultiplexFetcher:
    def __init__(self, worket_count = DEFAULT_WORKER_COUNT):
        self._worker = worket_count # Parallel async request count
        self._async_client = None

    async def _fetch_symbols(self, symbols, **kwargs):
        self._async_client = await AsyncClient.create()
        results = []

        try:
            for symbols_in_chunk in chunked_iterable(symbols, self._worker):
                res = await self._fetch_chunk(symbols_in_chunk, **kwargs)
                results.extend(res)
        finally:
            await self._async_client.close_connection()
        
        result_dict = { result[0]: result[1] for result in results }
        return result_dict
    
    async def _fetch_chunk(self, symbols, **kwargs):
        """
        creates a Future object for every symbol in the symbol_chunk.
        it awaits until all the Future objects returns.
        
        """
        tasks = []
        for symbol in symbols:
            task = asyncio.ensure_future(self._fetch_symbol(symbol, **kwargs))
            tasks.append(task)
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def _fetch_symbol(self, symbol,  **kwargs):
        raise NotImplementedError
    
    async def _get_function(self, symbol, **kwargs):
        raise NotImplementedError
    
    async def async_download(self, symbols, **kwargs):
        return await self._fetch_symbols(symbols, **kwargs)
    
    def download(self, symbols, **kwargs):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError as e:
            if str(e).startswith('There is no current event loop in thread'):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            else:
                raise
        res = loop.run_until_complete(self._fetch_symbols(symbols, **kwargs))
        return res
    

class OnlinePriceFetcher(MultiplexFetcher):
    def __init__(self, market, worket_count = DEFAULT_WORKER_COUNT):
        super().__init__(worket_count)
        self._market = market
        
    async def _fetch_symbol(self, symbol, **kwargs):
        """
        bottom-level function that sends HTTP request to Binance and awaits on response
        """
        try:
            price_data_raw = await self._get_function(symbol,  **kwargs)
            price_df = pd.DataFrame(price_data_raw)
            price_df = convert_price_data_types(price_df)
        except Exception as e:
            print(f'An error occured while fetching {symbol}. Error: {e}. {kwargs}')
            # raise Exception(f'An error occured while fetching {symbol}. Error: {e}')
            return symbol, str(e)
        return symbol, price_df


    async def _get_function(self, symbol, **kwargs):
        # TODO symbol unavailable hatasi geldiginde onu sonuca eklememek lazim
        if self._market == 'spot':
            return await self._async_client.get_historical_klines(symbol,  **kwargs)
        elif self._market == 'futures':
            return await self._async_client.futures_historical_klines(symbol,  **kwargs)
        else:
            raise ValueError(f"market type is invalid : {self._market}")

class OpenInterestFetcher(MultiplexFetcher):
    async def _get_function(self, **kwargs):
        # TODO symbol unavailable hatasi geldiginde onu sonuca eklememek lazim
        return await self._async_client.futures_open_interest_hist(**kwargs)
    
    async def _fetch_symbol(self, symbol, **kwargs):
        """
        bottom-level function that sends HTTP request to Binance and awaits on response
        """
        try:
            kwargs['symbol'] = symbol
            oi_raw = await self._get_function(**kwargs)
            oi_df = pd.DataFrame(oi_raw)
            oi_df = convert_oi_data(oi_df)
        except Exception as e:
            print(f'An error occured while fetching {symbol}. Error: {e}. {kwargs}')
            # raise Exception(f'An error occured while fetching {symbol}. Error: {e}')
            return symbol, str(e)
        return symbol, oi_df
        
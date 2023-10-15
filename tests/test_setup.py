import unittest

from ..fast_binance.fast_binance import OnlinePriceFetcher


class TestFunctionality(unittest.TestCase):
    def test_setup(self):
        pf = OnlinePriceFetcher('spot')
        res = pf.download(['SEIUSDT', 'FTTUSDT'], 
                          interval='1h', 
                          start_str='2023-01-01',
                          end_str='2023-08-01' )
        



if __name__ == '__main__':
    unittest.main()

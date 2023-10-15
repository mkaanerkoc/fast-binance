from fast_binance.fast_binance import OnlinePriceFetcher


def main():
    pf = OnlinePriceFetcher('spot')
    res = pf.download(['SEIUSDT', 'FTTUSDT', 'BTCUSDT'], 
                        interval='1h', 
                        start_str='2023-07-01',
                        end_str='2023-08-01' )
    print(res)
    

if __name__ == '__main__':
    main()
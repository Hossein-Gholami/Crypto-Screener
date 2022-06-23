import ccxt

binance = ccxt.binance()
_ = binance.load_markets()
symbols = binance.symbols

__all__ = ('binance', 'symbols', )
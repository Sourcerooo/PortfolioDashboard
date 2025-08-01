"""
Configuration module for the trading decision tool.
"""

# Default data download parameters
DEFAULT_DATA_PERIOD = "3y"  # 3 years of data
DEFAULT_DATA_INTERVAL = "1d"  # Daily data

# Tickers for the momentum strategy
MOMENTUM_TICKERS = ["SPY", "TIP", "BIL", "IEF"]

# Time periods for rate of change calculations (in days)
ROC_PERIODS = [30, 90, 180, 365, 395]  # 1, 3, 6, 12, 13 months

# Time windows for average price calculations (in days)
AVG_PRICE_WINDOWS = [10, 20, 50, 160, 200, 273]
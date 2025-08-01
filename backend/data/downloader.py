"""
Data downloader module for fetching stock data from Yahoo Finance.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from data.models import StockData
from config import DEFAULT_DATA_PERIOD, DEFAULT_DATA_INTERVAL


class DataDownloader:
    """Downloads stock data from Yahoo Finance."""

    def __init__(self):
        """Initialize the data downloader."""
        pass

    def download_data(self, symbol: str, period: str = DEFAULT_DATA_PERIOD,
                      interval: str = DEFAULT_DATA_INTERVAL) -> StockData:
        """
        Download stock data for a given symbol.
        
        Args:
            symbol: Stock ticker symbol
            period: Time period for data (e.g., '1y', '3y', '5y')
            interval: Data interval (e.g., '1d', '1wk', '1mo')
            
        Returns:
            StockData object containing the downloaded data
        """
        # Download data from Yahoo Finance
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=period, interval=interval)
        
        # Convert to our data structure
        stock_data = StockData(
            symbol=symbol,
            dates=history.index.tolist(),
            open_prices=history['Open'].tolist(),
            high_prices=history['High'].tolist(),
            low_prices=history['Low'].tolist(),
            close_prices=history['Close'].tolist(),
            volume=history['Volume'].tolist(),
            adjusted_close=history['Close'].tolist()  # Adjusted close in this case
        )
        
        return stock_data

    def download_multiple(self, symbols: list, period: str = DEFAULT_DATA_PERIOD,
                          interval: str = DEFAULT_DATA_INTERVAL) -> dict:
        """
        Download stock data for multiple symbols.
        
        Args:
            symbols: List of stock ticker symbols
            period: Time period for data
            interval: Data interval
            
        Returns:
            Dictionary mapping symbols to StockData objects
        """
        data = {}
        for symbol in symbols:
            data[symbol] = self.download_data(symbol, period, interval)
        return data
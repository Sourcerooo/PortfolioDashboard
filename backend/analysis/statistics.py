"""
Statistical analysis module for calculating stock data metrics.
"""

import pandas as pd
import numpy as np
from typing import List, Dict
from data.models import StockData
from config import ROC_PERIODS, AVG_PRICE_WINDOWS


class StockAnalyzer:
    """Performs statistical analysis on stock data."""

    def __init__(self):
        """Initialize the stock analyzer."""
        pass

    def calculate_rate_of_change(self, stock_data: StockData, periods: List[int] = ROC_PERIODS) -> Dict[str, float]:
        """
        Calculate absolute and percentage rate of change over specified periods.
        
        Args:
            stock_data: StockData object containing price data
            periods: List of periods in days to calculate ROC for
            
        Returns:
            Dictionary mapping period descriptions to (absolute, percentage) ROC tuples
        """
        if len(stock_data) == 0:
            return {}
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame({
            'Date': stock_data.dates,
            'Close': stock_data.close_prices
        })
        df = df.set_index('Date')
        
        results = {}
        latest_price = df['Close'].iloc[-1]
        
        for period in periods:
            # Skip if not enough data
            if len(df) < period:
                results[f"{period}_days"] = (0.0, 0.0)
                continue
            
            # Get price from 'period' days ago
            past_price = df['Close'].iloc[-period]
            
            # Calculate absolute and percentage change
            abs_change = latest_price - past_price
            pct_change = (abs_change / past_price) * 100 if past_price != 0 else 0.0
            
            results[f"{period}_days"] = (abs_change, pct_change)
        
        return results

    def calculate_average_price(self, stock_data: StockData, windows: List[int] = AVG_PRICE_WINDOWS) -> Dict[str, float]:
        """
        Calculate average price over specified windows.
        
        Args:
            stock_data: StockData object containing price data
            windows: List of window sizes in days to calculate averages for
            
        Returns:
            Dictionary mapping window descriptions to average prices
        """
        if len(stock_data) == 0:
            return {}
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame({
            'Date': stock_data.dates,
            'Close': stock_data.close_prices
        })
        df = df.set_index('Date')
        
        results = {}
        
        for window in windows:
            # Skip if not enough data
            if len(df) < window:
                results[f"{window}_days"] = 0.0
                continue
            
            # Calculate average over the window
            avg_price = df['Close'].iloc[-window:].mean()
            results[f"{window}_days"] = avg_price
        
        return results

    def get_price_at_date(self, stock_data: StockData, target_date) -> float:
        """
        Get the closing price at or before a specific date.
        
        Args:
            stock_data: StockData object containing price data
            target_date: Date to get price for
            
        Returns:
            Closing price at or before the target date
        """
        if len(stock_data) == 0:
            return 0.0
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame({
            'Date': stock_data.dates,
            'Close': stock_data.close_prices
        })
        df = df.set_index('Date')
        
        # Find the price at or before the target date
        try:
            price = df.loc[:target_date, 'Close'].iloc[-1]
            return price
        except IndexError:
            # If no data before target date, return the earliest available price
            return df['Close'].iloc[0]
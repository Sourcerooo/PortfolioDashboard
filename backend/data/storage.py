"""
Data storage module for saving and loading stock data to/from CSV files.
"""

import pandas as pd
import os
from pathlib import Path
from typing import Optional
from data.models import StockData
from data.downloader import DataDownloader
from config import DEFAULT_DATA_PERIOD, DEFAULT_DATA_INTERVAL


class DataStorage:
    """Handles storage of stock data in CSV files."""

    def __init__(self, data_dir: str = "data/csv"):
        """
        Initialize the data storage.
        
        Args:
            data_dir: Directory to store CSV files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.downloader = DataDownloader()

    def _get_file_path(self, symbol: str) -> Path:
        """
        Get the file path for a given symbol.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Path to the CSV file for the symbol
        """
        return self.data_dir / f"{symbol}.csv"

    def save_data(self, stock_data: StockData) -> None:
        """
        Save stock data to a CSV file.
        
        Args:
            stock_data: StockData object to save
        """
        file_path = self._get_file_path(stock_data.symbol)
        
        # Create DataFrame
        df = pd.DataFrame({
            'Date': stock_data.dates,
            'Open': stock_data.open_prices,
            'High': stock_data.high_prices,
            'Low': stock_data.low_prices,
            'Close': stock_data.close_prices,
            'Volume': stock_data.volume,
            'Adjusted_Close': stock_data.adjusted_close
        })
        
        # Save to CSV
        df.to_csv(file_path, index=False)

    def load_data(self, symbol: str) -> Optional[StockData]:
        """
        Load stock data from a CSV file.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            StockData object or None if file doesn't exist
        """
        file_path = self._get_file_path(symbol)
        
        if not file_path.exists():
            return None
            
        # Load from CSV
        df = pd.read_csv(file_path)
        
        # Convert to StockData
        stock_data = StockData(
            symbol=symbol,
            dates=pd.to_datetime(df['Date']).tolist(),
            open_prices=df['Open'].tolist(),
            high_prices=df['High'].tolist(),
            low_prices=df['Low'].tolist(),
            close_prices=df['Close'].tolist(),
            volume=df['Volume'].tolist(),
            adjusted_close=df['Adjusted_Close'].tolist()
        )
        
        return stock_data

    def update_data(self, symbol: str, period: str = DEFAULT_DATA_PERIOD,
                    interval: str = DEFAULT_DATA_INTERVAL) -> StockData:
        """
        Update data for a symbol by downloading new data and appending to existing data.
        
        Args:
            symbol: Stock ticker symbol
            period: Time period for data
            interval: Data interval
            
        Returns:
            Updated StockData object
        """
        # Try to load existing data
        existing_data = self.load_data(symbol)
        
        # Download latest data
        new_data = self.downloader.download_data(symbol, period, interval)
        
        if existing_data is None:
            # No existing data, save the new data
            self.save_data(new_data)
            return new_data
        
        # Combine existing and new data, removing duplicates
        combined_data = self._combine_data(existing_data, new_data)
        self.save_data(combined_data)
        return combined_data

    def _combine_data(self, existing: StockData, new: StockData) -> StockData:
        """
        Combine existing and new data, removing duplicates.
        
        Args:
            existing: Existing StockData
            new: New StockData
            
        Returns:
            Combined StockData
        """
        # Convert to DataFrames for easier manipulation
        existing_df = pd.DataFrame({
            'Date': existing.dates,
            'Open': existing.open_prices,
            'High': existing.high_prices,
            'Low': existing.low_prices,
            'Close': existing.close_prices,
            'Volume': existing.volume,
            'Adjusted_Close': existing.adjusted_close
        })
        
        new_df = pd.DataFrame({
            'Date': new.dates,
            'Open': new.open_prices,
            'High': new.high_prices,
            'Low': new.low_prices,
            'Close': new.close_prices,
            'Volume': new.volume,
            'Adjusted_Close': new.adjusted_close
        })
        
        # Combine and remove duplicates, keeping the latest data
        combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset='Date', keep='last')
        combined_df = combined_df.sort_values('Date')
        
        # Convert back to StockData
        combined_stock_data = StockData(
            symbol=existing.symbol,
            dates=combined_df['Date'].tolist(),
            open_prices=combined_df['Open'].tolist(),
            high_prices=combined_df['High'].tolist(),
            low_prices=combined_df['Low'].tolist(),
            close_prices=combined_df['Close'].tolist(),
            volume=combined_df['Volume'].tolist(),
            adjusted_close=combined_df['Adjusted_Close'].tolist()
        )
        
        return combined_stock_data
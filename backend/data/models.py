"""
Data models for the trading decision tool.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class StockData:
    """Represents stock price data for a single ticker."""
    symbol: str
    dates: List[datetime]
    open_prices: List[float]
    high_prices: List[float]
    low_prices: List[float]
    close_prices: List[float]
    volume: List[int]
    adjusted_close: List[float]

    def __len__(self) -> int:
        return len(self.dates)


@dataclass
class Recommendation:
    """Represents a trading recommendation from a strategy."""
    symbol: str
    allocation: float  # Percentage allocation (0-100)
    strategy_name: str
    timestamp: datetime


@dataclass
class MomentumResult:
    """Represents momentum calculation results."""
    symbol: str
    momentum_values: Dict[str, float]  # Period -> momentum value
    timestamp: datetime
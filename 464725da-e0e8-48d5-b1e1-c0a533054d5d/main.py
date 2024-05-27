from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize with the asset(s) you're interested in.
        self.tickers = ["XYZ"]  # Replace XYZ with the actual ticker you wish to trade.

    @property
    def assets(self):
        # Define which assets this strategy applies to.
        return self.tickers
    
    @property
    def interval(self):
        # The time interval for each data point, e.g., "1day" for daily data.
        return "1day"
    
    def run(self, data):
        # Here, implement the logic to decide when to buy or sell.
        
        # Assume we're dealing with daily data for simplicity.
        daily_data = data["ohlcv"]
        
        # Calculate the Simple Moving Average (SMA) for the past 10 days.
        # Please adjust the window size as needed for your strategy.
        sma10 = SMA("XYZ", daily_data, 10)  # "XYZ" is the asset ticker.
        
        allocation_dict = {}
        
        if len(sma10) > 0:
            current_price = daily_data[-1]["XYZ"]["close"]
            latest_sma = sma10[-1]

            # Decision rule: Buy if the latest price is above the SMA (signifying a positive trend),
            # otherwise hold no position.
            if current_price > latest_sma:
                log("Current price above SMA, buying signal.")
                allocation_dict["XYZ"] = 1.0  # Full allocation to this asset.
            else:
                log("Current price below SMA, selling/avoiding signal.")
                allocation_dict["XYZ"] = 0.0  # No allocation to this asset.
        
        return TargetAllocation(allocation_dict)
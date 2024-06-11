from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define a list of tickers representing companies in the fashion industry
        self.tickers = ["RL", "NKE", "LVMUY"]  # Example tickers: Ralph Lauren, Nike, LVMH
        
        # No additional data required for this strategy beyond what's provided by the technical indicators
        self.data_list = []
        
    @property
    def interval(self):
        # Utilize daily data for the SMA and RSI calculations
        return "1day"

    @property
    def assets(self):
        # The assets we are interested in trading (in this case, companies in the fashion industry)
        return self.tickers

    @property
    def data(self):
        # There's no additional data fetching setup here, as our data needs are covered by the technical indicators
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        
        for ticker in self.tickers:
            # Retrieve historical OHLCV data for the ticker
            ohlcv = data["ohlcv"]
            
            # Calculate the 50-day and 200-day Simple Moving Averages (SMA)
            sma_short_term = SMA(ticker, ohlcv, 50)
            sma_long_term = SMA(ticker, ohlcv, 200)
            
            # Calculate the Relative Strength Index (RSI) for a 14-day period
            rsi = RSI(ticker, ohlcv, 14)
            
            # Check if the 50-day SMA is above the 200-day SMA indicating a bullish trend
            # and ensure the RSI is below 70 to avoid overbought stocks
            if sma_short_term[-1] > sma_long_term[-1] and rsi[-1] < 70:
                # Allocate a portion of the portfolio to buy/hold the stock
                # Here, equally distribute the investment among selected tickers meeting the criteria
                # This allocation can be adjusted based on more sophisticated money management rules
                allocation_dict[ticker] = 1/len(self.tickers)
            else:
                # If conditions are not met, do not allocate capital to the stock
                allocation_dict[ticker] = 0

        # Return the target allocation for each ticker in the portfolio
        return TargetAllocation(allocation_dict)
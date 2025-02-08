import data_loader
import strategy
import logging
import pandas as pd
import json

# Configure logging
logging.basicConfig(filename='backtest.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define a logger
log = logging.getLogger(__name__)

class Context:
    def __init__(self, log):
        self.security = 'sh000001'  # Example security
        self.positions = {}
        self.cash = 10000000
        self.total_assets = self.cash
        self.g = type('Global', (object,), {})()  # Add a 'g' object
        self.log = log

    def get(self, security, default=0):
        return self.positions.get(security, default)

    def get_index_stocks(self, index_symbol):
        # Load index constituents from JSON file
        try:
            with open('/workspace/joinquant/index_constituents.json', 'r') as f:
                index_constituents = json.load(f)
            if index_symbol in index_constituents:
                logging.info(f"Getting index stocks for {index_symbol} from file")
                return index_constituents[index_symbol]
            else:
                logging.warning(f"Index symbol {index_symbol} not found in index_constituents.json")
                return []
        except FileNotFoundError:
            logging.error("index_constituents.json not found.")
            return []
        except json.JSONDecodeError:
            logging.error("index_constituents.json is not a valid JSON file.")
            return []

def order_target_value(context, security, target_value, price):
    current_value = context.positions.get(security, 0) * price
    amount_to_trade = (target_value - current_value) / price
    context.positions[security] = context.positions.get(security, 0) + amount_to_trade
    context.cash -= amount_to_trade * price
    context.total_assets = context.cash + sum(context.positions.values()) * price
    logging.info(f"Order: security={security}, target_value={target_value}, price={price}, amount_to_trade={amount_to_trade}")

def run_backtest():
    try:
        # Load data
        data = data_loader.load_data(symbol='sh000001', start_date='2023-04-24', end_date='2023-04-28')
        if data is None:
            logging.error("Failed to load data.")
            return

        # Create context
        context = Context(log)
        context.order_target_value = order_target_value

        # Initialize strategy
        strategy.initialize(context)

        # Backtesting loop
        for i in range(len(data)):
            # Get current data point
            current_data = data.iloc[i]
            price = current_data['Close']
            short_ma = data['Close'].rolling(window=context.g.short_window).mean()
            long_ma = data['Close'].rolling(window=context.g.long_window).mean()

            # Execute strategy
            strategy.handle_data(context, current_data, price, short_ma.iloc[-1], long_ma.iloc[-1])

            # Log the portfolio status
            logging.info(f"Date: {current_data.name}, Cash: {context.cash}, Total Assets: {context.total_assets}")

        logging.info("Backtesting completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during backtesting: {e}")

if __name__ == "__main__":
    run_backtest()
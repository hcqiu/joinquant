# JoinQuant Backtesting Framework

## Description

This project provides a Python framework for backtesting trading strategies. It allows you to define your own strategies and evaluate their performance using historical data.

## Files

*   `backtest.py`: Main script for running backtests.
*   `strategy.py`: Contains the base class for defining trading strategies.
*   `data_loader.py`: Handles loading historical data for backtesting.
*   `index_constituents.json`: Contains information about index constituents.
*   `backtest.log`: Log file for backtesting results.

## Usage

To run a backtest, execute the `backtest.py` script:

```bash
python backtest.py
```

## Example

Here's a simple example of how to define a trading strategy in `strategy.py`:

```python
class MyStrategy(Strategy):
    def __init__(self, data):
        super().__init__(data)

    def next(self):
        # Implement your trading logic here
        pass
```
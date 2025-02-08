def initialize(context, start_date, end_date, frequency, time):
    context.g.index_symbol = 'sh000300.XSHG'  # CSI 300 index
    context.g.top_n = 0.2  # Top 20%
    context.index_stocks = context.get_index_stocks(context.g.index_symbol)
    context.cash = 10000000  # Initial capital
    context.total_assets = context.cash
    context.g.start_date = start_date
    context.g.end_date = end_date
    context.g.frequency = frequency
    context.g.time = time
    context.log.info(f"Strategy initialized with index {context.g.index_symbol} and constituents {context.index_stocks}, initial_capital: {context.cash}, start_date: {start_date}, end_date: {end_date}, frequency: {frequency}, time: {time}")

def handle_data(context, data):
    # Get historical data for the index stocks
    historical_data = {}
    for stock in context.index_stocks:
        historical_data[stock] = context.history(security=stock, bar_count=5, frequency='1d', field='Close')

    # Compute previous day's price change
    price_change = {}
    for stock, data in historical_data.items():
        if not data.empty:
            price_change[stock] = data.pct_change().iloc[-1]  # Get the last price change
        else:
            price_change[stock] = 0  # If no data, set price change to 0

    # Rank stocks based on price change
    ranked_stocks = sorted(price_change, key=price_change.get, reverse=True)

    # Select top N stocks
    num_stocks_to_buy = int(len(context.index_stocks) * context.g.top_n)
    stocks_to_buy = ranked_stocks[:num_stocks_to_buy]

    # Buy the selected stocks
    for stock in stocks_to_buy:
        context.order_target_value(context, stock, 200000 / num_stocks_to_buy, context.price)

    context.log.info(f"Current holdings: {context.positions.get(context.security, 0)}, Cash: {context.cash}, Total Assets: {context.total_assets}")
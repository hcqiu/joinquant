def initialize(context):
    context.g.short_window = 2
    context.g.long_window = 5
    context.g.index_symbol = '000001.XSHG'  # Example index
    context.g.start_date = '2023-01-01'
    context.g.end_date = '2023-01-10'
    context.g.frequency = 'daily'
    context.g.time = 'close'
    context.g.initial_capital = 10000000  # Define initial capital
    context.index_stocks = context.get_index_stocks(context.g.index_symbol)
    context.log.info(f"Strategy initialized for {context.security} with index {context.g.index_symbol} and constituents {context.index_stocks}, start_date: {context.g.start_date}, end_date: {context.g.end_date}, frequency: {context.g.frequency}, time: {context.g.time}, initial_capital: {context.g.initial_capital}")

def handle_data(context, data, price, short_ma, long_ma):
    if short_ma > long_ma:
        context.order_target_value(context, context.security, 200000, price)  # Buy
    elif short_ma < long_ma:
        context.order_target_value(context, context.security, 0, price)  # Sell

    context.log.info(f"Current holdings: {context.positions.get(context.security, 0)}, Cash: {context.cash}, Total Assets: {context.total_assets}")
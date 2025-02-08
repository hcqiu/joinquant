def initialize(context):
    g.short_window = 2
    g.long_window = 5
    g.index_symbol = '000001.XSHG'  # Example index
    g.start_date = '2023-01-01'
    g.end_date = '2023-01-10'
    g.frequency = 'daily'
    g.time = 'close'
    g.initial_capital = 10000000  # Define initial capital
    context.index_stocks = get_index_stocks(g.index_symbol)
    log.info(f"Strategy initialized for {context.security} with index {g.index_symbol} and constituents {context.index_stocks}, start_date: {g.start_date}, end_date: {g.end_date}, frequency: {g.frequency}, time: {g.time}, initial_capital: {g.initial_capital}")

def handle_data(context, data, price):
    data['short_ma'] = data['Close'].rolling(window=g.short_window).mean()
    data['long_ma'] = data['Close'].rolling(window=g.long_window).mean()

    if data['short_ma'].iloc[-1] > data['long_ma'].iloc[-1]:
        order_target_value(context, context.security, 200000, price)  # Buy
    elif data['short_ma'].iloc[-1] < data['long_ma'].iloc[-1]:
        order_target_value(context, context.security, 0, price)  # Sell

    log.info(f"Current holdings: {context.positions.get(context.security, 0)}, Cash: {context.cash}, Total Assets: {context.total_assets}")

def initialize(context):
    context.g.index_symbol = 'sh000300.XSHG'  # CSI 300 index
    context.g.top_n = 0.2  # Top 20%
    context.index_stocks = context.get_index_stocks(context.g.index_symbol)
    context.cash = 10000000  # Initial capital
    context.total_assets = context.cash
    context.log.info(f"Strategy initialized with index {context.g.index_symbol} and constituents {context.index_stocks}, initial_capital: {context.cash}")

def handle_data(context, data):
    # Compute previous day's price change
    price_change = data['Close'].pct_change()

    # Rank stocks based on price change
    ranked_stocks = price_change.sort_values(ascending=False)

    # Select top N stocks
    num_stocks_to_buy = int(len(context.index_stocks) * context.g.top_n)
    stocks_to_buy = ranked_stocks.index[:num_stocks_to_buy]

    # Buy the selected stocks
    for stock in stocks_to_buy:
        context.order_target_value(context, stock, 200000 / num_stocks_to_buy, context.price)

    context.log.info(f"Current holdings: {context.positions.get(context.security, 0)}, Cash: {context.cash}, Total Assets: {context.total_assets}")
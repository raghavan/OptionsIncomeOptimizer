import yfinance as yf
from datetime import datetime, timedelta

def get_options_data(ticker, capital, limit_days):
    stock = yf.Ticker(ticker)
    current_price = stock.info['currentPrice']
    expiration_dates = stock.options

    suggestions = []
    today = datetime.today().date()
    limit_date = today + timedelta(days=limit_days)

    for expiration_date in expiration_dates:
        expiration_date_obj = datetime.strptime(expiration_date, '%Y-%m-%d').date()
        if expiration_date_obj <= limit_date:
            options_chain = stock.option_chain(expiration_date)
            puts = options_chain.puts

            for _, put in puts.iterrows():
                strike_price = put.strike
                if strike_price < current_price:
                    premium = put.lastPrice
                    contracts = int(capital // (put.strike * 100))
                    total_premium = premium * contracts * 100
                    days_to_expiration = (expiration_date_obj - today).days
                    daily_income = total_premium / days_to_expiration                    
                    if contracts > 0:
                        suggestion = {
                            'ticker': ticker,
                            'expiration_date': expiration_date,
                            'strike_price': strike_price,
                            'premium': premium,
                            'contracts': contracts,
                            'current_price': current_price,
                            'total_premium': total_premium,
                            'daily_income': daily_income
                        }
                        suggestions.append(suggestion)
    if suggestions:
        best_suggestion = max(suggestions, key=lambda x: x['daily_income'])
        return best_suggestion
    else:
        return None

# Example usage
tickers = ['AAPL','MSFT', 'PYXS']
capital = 10000
limit_days = 30

all_suggestions = []

for ticker in tickers:
    suggestions = get_options_data(ticker, capital, limit_days)
    if suggestions is not None:
        all_suggestions.append(suggestions)


if all_suggestions:
    sorted_suggestions = sorted(all_suggestions, key=lambda x: x['daily_income'], reverse=True)
    
    print("Sorted Suggestions:")
    for suggestion in sorted_suggestions:
        print(f"Ticker: {suggestion['ticker']}")
        print(f"Expiration Date: {suggestion['expiration_date']}")
        print(f"Strike Price: {suggestion['strike_price']}")
        print(f"Current Price: {suggestion['current_price']}")
        print(f"Premium Received: {suggestion['premium']}")
        print(f"Contracts: {suggestion['contracts']}")
        print(f"Total Premium Received: {suggestion['total_premium']}"),
        print(f"Daily Income:{suggestion['daily_income']}")
        print("---")
else:
    print("No suitable options found.")
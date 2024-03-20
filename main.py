import robin_stocks.robinhood as rh
import os
import json
import requests
from datetime import datetime

base_path = os.path.abspath(os.path.dirname(__file__))
with open(base_path+'/config.json') as config_file:
    config = json.load(config_file)

def get_buy_tickers():
    api_endpoint = config["api_endpoint"]
    api_key = config["api_key"]
    res = requests.get(api_endpoint + "&api_key=" + api_key)
    response = res.json()["data"]
    tickers = []
    for obj in response:
        tickers.append(obj["ticker"])
    return tickers

if __name__ == "__main__":
    rh.login(config["robinhood"]["username"], config["robinhood"]["password"])

    total_value = float(rh.load_portfolio_profile()["market_value"])
    cash = float(rh.load_account_profile()["cash"])

    print(rh.get_open_stock_positions())

    to_buy = get_buy_tickers()

    holding_period = int(config["holding_period"])

    amount_per_name = min((total_value + cash) / (len(to_buy) * holding_period), cash / len(to_buy))

    current_positions = rh.get_open_stock_positions()

    # find to sell
    to_sell = {}
    for position in current_positions:
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        date = datetime.strptime(position["created_at"], f)
        if (datetime.now() - date).days > holding_period:
            res = requests.get(position["instrument"])
            ticker = res.json()["symbol"]
            if ticker in to_buy:
                to_buy.remove(ticker)
            else:
                to_sell[ticker] = position["quantity"]
    for ticker, quantity in to_sell:
        print("Selling", ticker)
        rh.order_sell_fractional_by_quantity(ticker, quantity)
    for ticker in to_buy:
        print("Buying", amount_per_name, "worth of", ticker)
        rh.order_buy_fractional_by_price(ticker, amount_per_name)

    rh.logout()

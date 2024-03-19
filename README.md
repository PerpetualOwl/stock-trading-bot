# stock-trading-bot
Stock Trading Bot which gets what to buy from external apis

## Simple Architecture

Check if is before market open on a trading day, otherwise exit and skip rest
Check if market orders already exist on brokerage account, if so exit and skip rest
Otherwise first handle sell orders, check orders from 5 trading days ago
Then use API to get new buys
If there is overlap, don't do anything - otherwise sell the sells and buy the buys all market orders
exit


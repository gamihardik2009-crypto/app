import yfinance as yf

ticker = "TATASTEEL.NS"
stock = yf.Ticker(ticker)

# Current price
price = stock.info["currentPrice"]
print("Current Price:", price)

# Financial data
income = stock.financials
balance = stock.balance_sheet

# Latest year
latest = income.columns[0]

# Income values
revenue = income.loc["Total Revenue", latest]
ebitda = income.loc["EBITDA", latest]
pat = income.loc["Net Income", latest]

# Balance values
assets = balance.loc["Total Assets", latest]
debt = balance.loc["Total Debt", latest]

# Equity
equity = assets - debt

print("Revenue:", revenue)
print("EBITDA:", ebitda)
print("PAT:", pat)
print("Equity:", equity)

# Ratios
de_ratio = debt / equity
ebitda_margin = ebitda / revenue

print("Debt/Equity:", round(de_ratio, 2))
print("EBITDA Margin:", round(ebitda_margin * 100, 2), "%")

# Intrinsic value (simple MVP logic)
intrinsic = equity / 1e9

print("Intrinsic Value (Approx):", round(intrinsic, 2))

# Signal logic
if de_ratio < 0.5 and ebitda_margin > 0.15 and price < intrinsic:
    signal = "BUY"
elif de_ratio > 1 or ebitda_margin < 0.1:
    signal = "SELL"
else:
    signal = "HOLD"

print("Signal:", signal)

import streamlit as st
import yfinance as yf

st.title("Fundamental Health Checker")

ticker = st.text_input("Enter stock ticker", "TATASTEEL.NS")

if st.button("Run Analysis"):
    stock = yf.Ticker(ticker)
    price = stock.info.get("currentPrice", "N/A")

    income = stock.financials
    balance = stock.balance_sheet
    latest = income.columns[0]

    revenue = income.loc["Total Revenue", latest]
    ebitda = income.loc["EBITDA", latest]
    debt = balance.loc["Total Debt", latest]
    assets = balance.loc["Total Assets", latest]
    equity = assets - debt

    de_ratio = debt / equity
    ebitda_margin = ebitda / revenue
    intrinsic = equity / 1e9

    st.write("Price:", price)
    st.write("Revenue:", revenue)
    st.write("EBITDA:", ebitda)
    st.write("Equity:", equity)
    st.write("Debt/Equity:", round(de_ratio, 2))
    st.write("EBITDA Margin (%):", round(ebitda_margin * 100, 2))
    st.write("Intrinsic (approx):", round(intrinsic,2))

    if de_ratio < 0.5 and ebitda_margin > 0.15 and price < intrinsic:
        signal = "BUY"
    elif de_ratio > 1 or ebitda_margin < 0.1:
        signal = "SELL"
    else:
        signal = "HOLD"

    st.write("Signal:", signal)


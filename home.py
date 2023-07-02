from logic import dfEquity
import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

def main():
    st.title("Portfolio Dashboard")
    starting_cash = 1000000
    st.sidebar.markdown("Input the assets in the portfolio below:")
    ticker = st.sidebar.text_input("Ticker")
    amount_of_shares = st.sidebar.number_input("Amount of Shares", min_value=1)
    asset_type = st.sidebar.selectbox("Type", ["Buy", "Short"])
    open_date = st.sidebar.date_input("Position Purchase Date")
    close_date = st.sidebar.date_input("Position Close (current date is default)")
    industry_select = st.sidebar.selectbox('Select Industry', dfEquity)

    add_asset_button = st.sidebar.button("Add Asset")
    undo_button = st.sidebar.button("Undo Asset")

    if 'asset_list' not in st.session_state:
        st.session_state.asset_list = []

    if add_asset_button:
        st.session_state.asset_list.append({"Ticker": ticker.upper(),
                                            "Amount of Shares": amount_of_shares,
                                            "Type": asset_type, "Industry": industry_select, "Position Open": open_date, "Position Close": close_date })

    if undo_button and st.session_state.asset_list:
        st.session_state.asset_list.pop()

    st.table(st.session_state.asset_list)

    # Create a dataframe to hold historical price data for all assets in the portfolio
    price_data = pd.DataFrame()

    # Loop over all assets in the portfolio
    for asset in st.session_state.asset_list:
        # Fetch historical price data for the asset
        stock_data = yf.download(asset["Ticker"], start=asset["Position Open"], end=asset["Position Close"])
        # Calculate the asset value over time and add it to the price data dataframe
        if asset["Type"] == "Buy":
            price_data[asset["Ticker"]] = stock_data['Close'] * asset["Amount of Shares"]
        else:  # asset is shorted
            price_data[asset["Ticker"]] = (stock_data['Close'] * asset["Amount of Shares"])
    # Calculate the portfolio value over time
    # Calculate the portfolio ROI by summing ROIs of individual assets
    portfolio_value = price_data.sum(axis=1)
    total_value_added = portfolio_value.iloc[-1] + starting_cash
    delta_value = ((st.session_state.last_total_value / starting_cash) * 100)
    st.session_state.last_total_value = total_value_added



    # Create a plotly line graph for portfolio value
    fig = px.line(portfolio_value, title='Portfolio Historical Performance')
    fig.update_layout(
    autosize=True,
    width=700,
    height=600,
)
    st.plotly_chart(fig)
    st.metric(label="Current Portfolio Value", 
            value= f'${total_value_added:,.2f}', 
            delta= f'{delta_value:,.2f}%')

if __name__ == "__main__":
    main()

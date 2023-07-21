from logic import dfEquity
import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, timezone  # Import timezone from datetime module
import pyfolio as pf
import warnings
warnings.filterwarnings('ignore')

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

    # Initialize the asset_list in session state
    if 'asset_list' not in st.session_state:
        st.session_state.asset_list = []

    if add_asset_button:
        st.session_state.asset_list.append({"Ticker": ticker.upper(),
                                            "Amount of Shares": amount_of_shares,
                                            "Type": asset_type, "Industry": industry_select, "Position Open": open_date, "Position Close": close_date })

    if undo_button and st.session_state.asset_list:
        st.session_state.asset_list.pop()

    st.table(st.session_state.asset_list)

    if st.session_state.asset_list:
        price_data = pd.DataFrame()

        for asset in st.session_state.asset_list:
            # Convert open_date and close_date to datetime objects and set them to UTC timezone
            open_date_utc = datetime(asset["Position Open"].year, asset["Position Open"].month, asset["Position Open"].day, tzinfo=timezone.utc)
            close_date_utc = datetime(asset["Position Close"].year, asset["Position Close"].month, asset["Position Close"].day, tzinfo=timezone.utc)

            stock_data = yf.download(asset["Ticker"], start=open_date_utc, end=close_date_utc)
            if not stock_data.empty:
                if asset["Type"] == "Buy":
                    price_data[asset["Ticker"]] = stock_data['Close'] * asset["Amount of Shares"]
                else:
                    price_data[asset["Ticker"]] = (stock_data['Close'] * asset["Amount of Shares"]) * -1

        if not price_data.empty:
            portfolio_value = price_data.sum(axis=1)
            if not portfolio_value.empty:
                total_value_added = portfolio_value.iloc[-1] + starting_cash
                if 'last_total_value' in st.session_state:
                    delta_value = ((total_value_added / starting_cash) - 1) * 100
                else:
                    delta_value = 0 
                st.session_state.last_total_value = total_value_added

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

                latest_values = price_data.iloc[-1]
                fig = px.pie(values=latest_values, names=latest_values.index, title='Portfolio Allocation')
                fig.update_layout(autosize=True, width=900, height=700)
                st.plotly_chart(fig)
    else:
        st.warning("Please add at least one asset to the portfolio.")

if __name__ == "__main__":
    main()

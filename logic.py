import financedatabase as fd
import pandas as pd
import yfinance as yf


# Sector dataframe
equities = fd.Equities()
equities_industry_groups = equities.options('industry_group')
dfEquity = pd.DataFrame(equities_industry_groups)

#pie chart weighting logic

fb = yf.Ticker('FB')
history = fb.history('max')
history.index = history.index.tz_localize('utc')
history.info()


pf.create_returns_tear_sheet(returns, live_start_date='2020-1-1')




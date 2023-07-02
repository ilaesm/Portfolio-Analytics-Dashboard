import financedatabase as fd
import pandas as pd
import yfinance as yf


# Sector dataframe
equities = fd.Equities()
equities_industry_groups = equities.options('industry_group')
dfEquity = pd.DataFrame(equities_industry_groups)

#pie chart weighting logic








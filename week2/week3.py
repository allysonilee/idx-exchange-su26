import pandas as pd

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (mortgage.groupby('year_month')['rate_30yr_fixed'].mean().reset_index())

sold = pd.read_csv("C:/Users/izlal/IDXExchange_SU26/week2/CRMLSSoldAll.csv", )

listings = pd.read_csv("C:/Users/izlal/IDXExchange_SU26/week2/CRMLSListingAll.csv")

# Sold dataset — key off CloseDate
sold['year_month'] = pd.to_datetime(sold['CloseDate'], format = 'mixed').dt.to_period('M')
# Listings dataset — key off ListingContractDate
listings['year_month'] = pd.to_datetime(listings['ListingContractDate'], format = 'mixed').dt.to_period('M')

sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
listings_with_rates = listings.merge(mortgage_monthly, on='year_month', how='left')

# Check for any unmatched rows (rate should not be null)
print("Sold null mortgage rates: ", sold_with_rates['rate_30yr_fixed'].isnull().sum())
print("Listings null mortgage rates: ", listings_with_rates['rate_30yr_fixed'].isnull().sum())

# Preview
print(sold_with_rates[['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']].head())

sold_with_rates.to_csv("CRMLSSoldwRates")
listings_with_rates.to_csv("CRMLSListingwRates")

# January 2024 to May 2026 Data Analysis
###
# Data Validation:
# Sold null mortgage rates:  0
# Listings null mortgage rates: 0
###
# Sold with Rates Dataframe Preview:
#     CloseDate year_month  ClosePrice  rate_30yr_fixed
# 0  2024-01-26    2024-01    240000.0           6.6425
# 1  2024-01-24    2024-01       950.0           6.6425
# 2  2024-01-16    2024-01     45000.0           6.6425
# 3  2024-01-08    2024-01    141500.0           6.6425
# 4  2024-01-17    2024-01     15000.0           6.6425
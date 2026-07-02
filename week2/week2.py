import pandas as pd
import numpy as np

sold = pd.read_csv("C:/Users/izlal/IDXExchange_SU26/week1/ConcatenatedCRMLSSold.csv")

# Identify numbers of rows and columns
sold_rows = len(sold)
print("Sold Number of Rows: ", sold_rows)

sold_cols = len(sold.columns)
print("Sold Number of Columns: ", sold_cols)

# Review column data types
sold_dtypes = sold.dtypes.astype(str).unique().tolist()
print("Sold Column Datatypes: ", sold_dtypes)

# Document unique Property Types found
property_types = sold['PropertyType'].unique()
print(property_types)

# Apply filtering logic
sold_filtered = sold[sold.PropertyType == 'Residential']

# Identify high missing columns
sold_filtered.isna().sum().loc[lambda s: s > 0].sort_values(ascending = False)

# Calculate missing counts and percentages per column (null count summary table)
missing_sum = pd.DataFrame({
    "Null Count": sold_filtered.isna().sum(),
    "Null Percentage": (sold_filtered.isna().mean() * 100).round(2)
})

# Flag columns with >90% missing values
missing_sum["Flag"] = missing_sum["Null Percentage"] > 90
print("Flagged missing columns: ", missing_sum.index[missing_sum["Flag"]])

# Produce a numeric distribution summary (min, max, mean, median, percentiles) for ClosePrice, LivingArea, and DaysOnMarket
target_cols = ["ClosePrice", "LivingArea", "DaysOnMarket"]
for col in target_cols:
    print(sold_filtered[col].describe())

# Save the filtered dataset as a new CSV
sold_filtered.to_csv("CRMLSSoldFiltered.csv")

# January 2024 to May 2026 Sold Data Analysis
###
# Sold Number of Rows:  430445
# Sold Number of Columns:  83
# Sold Column Datatypes:  ['int64', 'str', 'object', 'float64']
# Sold Property Types: 'BusinessOpportunity', 'CommercialLease', 'CommercialSale', 'Land', 'ManufacturedInPark', 'ResidentialIncome', 'ResidentialLease')
# Flagged Missing Columns: 'WaterfrontYN', 'BasementYN', 'FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount', 'BuilderName', 'TaxYear', 'BuildingAreaTotal', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName', 'BelowGradeFinishedArea', 'BusinessType', 'CoveredSpaces', 'LotSizeDimensions', 'MiddleOrJuniorSchoolDistrict'
###
# Numeric Distribution Summary: 
# ClosePrice:
# count    4.304430e+05
# mean     1.193117e+06
# std      6.174121e+06
# min      0.000000e+00
# 25%      5.750000e+05
# 50%      8.250000e+05
# 75%      1.300000e+06
# max      9.895000e+08
##
# LivingArea: 
# count    4.302000e+05
# mean     1.904068e+03
# std      2.596802e+04
# min      0.000000e+00
# 25%      1.248000e+03
# 50%      1.644000e+03
# 75%      2.221000e+03
# max      1.702132e+07
##
# DaysOnMarket:
# count    430445.000000
# mean         37.333627
# std          53.668097
# min        -288.000000
# 25%           8.000000
# 50%          18.000000
# 75%          48.000000
# max       12430.000000
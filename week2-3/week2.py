import pandas as pd
import numpy as np

sold = pd.read_csv("C:/Users/izlal/IDXExchange_SU26/week2/CRMLSSoldAll.csv")

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
    print(sold_filtered[col].describe().apply(lambda x: f"{x:.2f}"))

# Save the filtered dataset as a new CSV
sold_filtered.to_csv("CRMLSSoldFiltered.csv")

# January 2024 to May 2026 Sold Data Analysis
###
# Sold Number of Rows:  639916
# Sold Number of Columns:  83
# Sold Column Datatypes:  ['int64', 'str', 'object', 'float64']
# Sold Property Types: ['Residential', 'CommercialLease', 'Land', 'ResidentialLease', 'ManufacturedInPark', 'ResidentialIncome', 'CommercialSale', 'BusinessOpportunity']
# Flagged Missing Columns: ['WaterfrontYN', 'BasementYN', 'FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount', 'BuilderName', 'TaxYear', 'BuildingAreaTotal', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName', 'BelowGradeFinishedArea', 'BusinessType', 'CoveredSpaces', 'LotSizeDimensions', 'MiddleOrJuniorSchoolDistrict']
###
# Numeric Distribution Summary: 
# ClosePrice:
# count       430443.00
# mean       1193116.77
# std        6174121.01
# min              0.00
# 25%         575000.00
# 50%         825000.00
# 75%        1300000.00
# max      989500000.00
##
# LivingArea: 
# count      430200.00
# mean         1904.07
# std         25968.02
# min             0.00
# 25%          1248.00
# 50%          1644.00
# 75%          2221.00
# max      17021321.00
##
# DaysOnMarket:
# count    430445.00
# mean         37.33
# std          53.67
# min        -288.00
# 25%           8.00
# 50%          18.00
# 75%          48.00
# max       12430.00
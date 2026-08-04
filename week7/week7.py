import pandas as pd

# Import relevant CRMLSListing and CRMLSSold CSVs
listings = pd.read_csv("CSVs/CRMLSListingwDistrict.csv", low_memory = False)
sold = pd.read_csv("CSVs/CRMLSSoldwDistrict.csv", low_memory = False)

# Key numeric fields for IQR filtering
target_cols = ['ClosePrice', 'LivingArea', 'DaysOnMarket']

# Dataset size and median values before filtering
print('Before filtering: ')
print(f'Listings size: {len(listings)}')
for col in target_cols: 
    print(f'Listing {col} median: {listings[col].median()}')
print(f'Sold size: {len(sold)}')
for col in target_cols: 
    print(f'Sold {col} median: {sold[col].median()}')

# Listings IQR filter
listings_filtered = listings.copy()
for col in target_cols:
    Q1 = listings[col].quantile(0.25)
    Q3 = listings[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    # Create flag columns in the original dataset
    listings[f'outlier_flagged_{col}'] = (listings[col] < lower) | (listings[col] > upper)
    # Create a filtered dataset
    listings_filtered = listings_filtered[(listings_filtered[col] >= lower) & (listings_filtered[col] <= upper)]

# Sold IQR filter
sold_filtered = sold.copy()
for col in target_cols:
    Q1 = sold[col].quantile(0.25)
    Q3 = sold[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    # Create flag columns in the original dataset
    sold[f'outlier_flagged_{col}'] = (sold[col] < lower) | (sold[col] > upper)
    # Create a filtered dataset
    sold_filtered = sold_filtered[(sold_filtered[col] >= lower) & (sold_filtered[col] <= upper)]

# Dataset size and median values after filtering
print('After filtering: ')
print(f'Listings size: {len(listings_filtered)}')
for col in target_cols: 
    print(f'Listing {col} median: {listings_filtered[col].median()}')
print(f'Sold size: {len(sold_filtered)}')
for col in target_cols: 
    print(f'Sold {col} median: {sold_filtered[col].median()}')

listings_filtered.to_csv("CSVs/CRMLSListingCleanFiltered.csv", index = False)
listings.to_csv("CSVs/CRMLSListingFlagged.csv", index = False)

sold_filtered.to_csv("CSVs/CRMLSSoldCleanFiltered.csv", index = False)
sold.to_csv("CSVs/CRMLSSoldFlagged.csv", index = False)

#--------------------------------------------#
# Summary of Dataset Size and Median Values
#--------------------------------------------#
### Before filtering:
# Listings size: 852686
# Listing ClosePrice median: 530000.0
# Listing LivingArea median: 1604.0
# Listing DaysOnMarket median: 10.0
##
# Sold size: 645045
# Sold ClosePrice median: 621297.5
# Sold LivingArea median: 1583.0
# Sold DaysOnMarket median: 22.0
#--------------------------------------------#
### After filtering:
# Listings size: 548683
# Listing ClosePrice median: 530000.0
# Listing LivingArea median: 1604.0
# Listing DaysOnMarket median: 8.0
##
# Sold size: 551658
# Sold ClosePrice median: 600000.0
# Sold LivingArea median: 1565.0
# Sold DaysOnMarket median: 19.0
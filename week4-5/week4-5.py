import pandas as pd
import geopandas as gpd

# Import CRMLSListings and CRMLSSold CSVs
listings = pd.read_csv("C:/Users/izlal/IDXExchange_SU26/week2-3/CRMLSListingwRates.csv", low_memory = False)
sold = pd.read_csv("C:/Users/izlal/IDXExchange_SU26/week2-3/CRMLSSoldwRates.csv", low_memory = False)

# Before row & col counts: 
print(f"Listings rows before cleaning: {len(listings)}")
print(f"Listings columns before cleaning: {len(listings.columns)}")
print(f"Sold rows before cleaning: {len(sold)}")
print(f"Sold columns before cleaning: {len(sold.columns)}")

# Convert date fields to datetime format (CloseDate, PurchaseContractDate, ListingContractDate, ContractStatusChangeDate)
date_fields = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']
for field in date_fields: 
    listings[field] = pd.to_datetime(listings[field], format = 'mixed')
    sold[field] = pd.to_datetime(sold[field], format = 'mixed')

# Data Consistency Check: 
# Validate the logical order of date fields: ListingContractDate should precede PurchaseContractDate, which should precede CloseDate. Create boolean flag columns to mark records that violate these rules:
listings['listing_after_close_flag'] = listings['CloseDate'] < listings['ListingContractDate']
listings['purchase_after_close_flag'] = listings['CloseDate'] < listings['PurchaseContractDate']
listings['negative_timeline_flag'] = (listings['listing_after_close_flag'] | listings['purchase_after_close_flag'])

sold['listing_after_close_flag'] = sold['CloseDate'] < sold['ListingContractDate']
sold['purchase_after_close_flag'] = sold['CloseDate'] < sold['PurchaseContractDate']
sold['negative_timeline_flag'] = (sold['listing_after_close_flag'] | sold['purchase_after_close_flag'])

print("Listings: ")
print(f"Flagged listing after close: {sum(listings['listing_after_close_flag'])}")
print(f"Flagged purchase after close: {sum(listings['purchase_after_close_flag'])}")
print(f"Flagged negative timeline: {sum(listings['negative_timeline_flag'])}")

print("Sold: ")
print(f"Flagged listing after close: {sum(sold['listing_after_close_flag'])}")
print(f"Flagged purchase after close: {sum(sold['purchase_after_close_flag'])}")
print(f"Flagged negative timeline: {sum(sold['negative_timeline_flag'])}")

# Remove flagged illogical date rows
listings = listings[~(listings['listing_after_close_flag']) & ~(listings['purchase_after_close_flag'])]
sold = sold[~(sold['listing_after_close_flag']) & ~(sold['purchase_after_close_flag'])]

# Remove or flag invalid numeric values: ClosePrice <= 0, LivingArea <= 0, DaysOnMarket < 0, negative Bedrooms or Bathrooms
listings['closeprice_flag'] = (listings['ClosePrice'] <= 0)
listings['livingarea_flag'] = (listings['LivingArea'] <= 0)
listings['daysonmarket_flag'] = (listings['DaysOnMarket'] < 0)
listings['neg_rooms_flag'] = (listings['BathroomsTotalInteger'] < 0) | (listings['BedroomsTotal'] < 0)

sold['closeprice_flag'] = (sold['ClosePrice'] <= 0)
sold['livingarea_flag'] = (sold['LivingArea'] <= 0)
sold['daysonmarket_flag'] = (sold['DaysOnMarket'] < 0)
sold['neg_rooms_flag'] = (sold['BathroomsTotalInteger'] < 0) | (sold['BedroomsTotal'] < 0)

print("Listings: ")
print(f"Flagged Close Price: {sum(listings['closeprice_flag'])}")
print(f"Flagged Living Area: {sum(listings['livingarea_flag'])}")
print(f"Flagged Days on Market: {sum(listings['daysonmarket_flag'])}")
print(f"Flagged Negative Rooms: {sum(listings['neg_rooms_flag'])}")

print("Sold: ")
print(f"Flagged Close Price: {sum(sold['closeprice_flag'])}")
print(f"Flagged Living Area: {sum(sold['livingarea_flag'])}")
print(f"Flagged Days on Market: {sum(sold['daysonmarket_flag'])}")
print(f"Flagged Negative Rooms: {sum(sold['neg_rooms_flag'])}")

# Remove unnecessary or redundant columns
# Flagged Missing Columns (Observed in Week 2): ['WaterfrontYN', 'BasementYN', 'FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount', 'BuilderName', 'TaxYear', 'BuildingAreaTotal', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName', 'BelowGradeFinishedArea', 'BusinessType', 'CoveredSpaces', 'LotSizeDimensions', 'MiddleOrJuniorSchoolDistrict']
listings = listings.drop(columns = ['FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount', 'BuilderName', 'TaxYear', 'BuildingAreaTotal', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName', 'BelowGradeFinishedArea', 'BusinessType', 'CoveredSpaces', 'LotSizeDimensions', 'MiddleOrJuniorSchoolDistrict'])
listings = listings.loc[:, ~listings.columns.duplicated()]

sold = sold.drop(columns = ['WaterfrontYN', 'BasementYN', 'FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount', 'BuilderName', 'TaxYear', 'BuildingAreaTotal', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName', 'BelowGradeFinishedArea', 'BusinessType', 'CoveredSpaces', 'LotSizeDimensions', 'MiddleOrJuniorSchoolDistrict'])
sold = sold.loc[:, ~sold.columns.duplicated()]

# Ensure numeric fields are properly typed
num_fields = ['AssociationFee', 'BathroomsTotalInteger', 'BedroomsTotal', 'ClosePrice', 'DaysOnMarket', 'GarageSpaces', 'Latitude', 'ListingKeyNumeric', 'ListPrice', 'LivingArea', 'Longitude', 'LotSizeAcres', 'LotSizeArea', 'LotSizeSquareFeet', 'MainLevelBedrooms', 'OriginalListPrice', 'ParkingTotal', 'Stories', 'StreetNumberNumeric', 'YearBuilt'] # excludes flagged missing columns
print("Listings: ")
for field in num_fields:
    print(f"{field}: {listings[field].dtype}")

print("Sold: ")
for field in num_fields:
    print(f"{field}: {sold[field].dtype}")

### Geographic Data Check: 
# Flag records with missing coordinates (Latitude or Longitude is null)
listings['missing_coords'] = listings['Latitude'].isna() | listings['Longitude'].isna()
sold['missing_coords'] = sold['Latitude'].isna() | sold['Longitude'].isna()

# Flag Latitude = 0 or Longitude = 0 (sentinel null values)
listings['null_coords'] = (listings['Latitude'] == 0) | (listings['Longitude'] == 0)
sold['null_coords'] = (sold['Latitude'] == 0) | (sold['Longitude'] == 0)

# Flag Longitude > 0 errors (California coordinates should be negative)
listings['oob_coords'] = (listings['Longitude'] > 0)
sold['oob_coords'] = (sold['Longitude'] > 0)

# Flag out-of-state or implausible coordinates
listings['oos_coords'] = (listings['Latitude'] < 32.5) | (listings['Latitude'] > 42) | (listings['Longitude'] > -114.13) | (listings['Longitude'] < -124.48)
listings['imp_coords'] = (listings['Latitude'] < -90) | (listings['Latitude'] > 90) | (listings['Longitude'] > 180) | (listings['Longitude'] < -180)

sold['oos_coords'] = (sold['Latitude'] < 32.5) | (sold['Latitude'] > 42) | (sold['Longitude'] > -114.13) | (sold['Longitude'] < -124.48)
sold['imp_coords'] = (sold['Latitude'] < -90) | (sold['Latitude'] > 90) | (sold['Longitude'] > 180) | (sold['Longitude'] < -180)

print("Listings: ")
print(f"Missing Coordinates: {sum(listings['missing_coords'])}")
print(f"Flagged Null Coordinates: {sum(listings['null_coords'])}")
print(f"Out-of-bound Coordinates: {sum(listings['oob_coords'])}")
print(f"Out-of-state Coordinates: {sum(listings['oos_coords'])}")
print(f"Implausible Coordinates: {sum(listings['imp_coords'])}")

print("Sold: ")
print(f"Missing Coordinates: {sum(sold['missing_coords'])}")
print(f"Flagged Null Coordinates: {sum(sold['null_coords'])}")
print(f"Out-of-bound Coordinates: {sum(sold['oob_coords'])}")
print(f"Out-of-state Coordinates: {sum(sold['oos_coords'])}")
print(f"Implausible Coordinates: {sum(sold['imp_coords'])}")

# Remove flagged rows: 
listings = listings[~(listings['missing_coords']) & ~(listings['null_coords']) & ~(listings['oob_coords']) & ~(listings['oos_coords']) & ~(listings['imp_coords'])]
sold = sold[~(sold['missing_coords']) & ~(sold['null_coords']) & ~(sold['oob_coords']) & ~(sold['oos_coords']) & ~(sold['imp_coords'])]

# Handle missing values appropriately
num_listings = listings.select_dtypes(include=['number']).columns
listings[num_listings] = listings[num_listings].fillna(listings[num_listings].median())
obj_listings = listings.select_dtypes(include=['str']).columns
listings[obj_listings] = listings[obj_listings].fillna("Missing")

num_sold = sold.select_dtypes(include=['number']).columns
sold[num_sold] = sold[num_sold].fillna(sold[num_sold].median())
obj_sold = sold.select_dtypes(include=['str']).columns
sold[obj_sold] = sold[obj_sold].fillna("Missing")

### Add school district mapping
# Read California school district boundary GeoJSON
districts_gdf = gpd.read_file("C:/Users/izlal/IDXExchange_SU26/week4-5/DistrictAreas2526_-284845464123469011.geojson")

# Filter the school district dataset to only include DistrictType == "Unified"
districts_gdf = districts_gdf[districts_gdf["DistrictType"] == "Unified"]
districts_gdf.head()

districts_gdf = districts_gdf.to_crs(crs = "EPSG:4326")

# Remove original CSV index columns to prevent index duplication
listings = listings.loc[:, ~listings.columns.str.contains('^Unnamed')]
sold = sold.loc[:, ~sold.columns.str.contains('^Unnamed')]

# Convert each property’s Latitude and Longitude into a geographic point
listings_gdf = gpd.GeoDataFrame(listings, geometry = gpd.points_from_xy(listings["Longitude"], listings["Latitude"]), crs="EPSG:4326")
sold_gdf = gpd.GeoDataFrame(sold, geometry = gpd.points_from_xy(sold["Longitude"], sold["Latitude"]), crs="EPSG:4326")

# Perform a spatial join (gpd.sjoin) to determine which Unified School District polygon contains each property
listings_joined = gpd.sjoin(listings_gdf, districts_gdf, how = "left", predicate = "within")
sold_joined = gpd.sjoin(sold_gdf, districts_gdf, how = "left", predicate = "within")

# Drop gpd.sjoin index column
listings_joined = listings_joined.drop(columns=["index_right"], errors="ignore")
sold_joined = sold_joined.drop(columns=["index_right"], errors="ignore")

# Add the resulting DistrictName as a new column in your dataset
listings_df = pd.DataFrame(listings_joined)
sold_df = pd.DataFrame(sold_joined)

# After row & col counts: 
print(f"Listings rows after cleaning: {len(listings_df)}")
print(f"Listings columns after cleaning: {len(listings_df.columns)}")
print(f"Sold rows after cleaning: {len(sold_df)}")
print(f"Sold columns after cleaning: {len(sold_df.columns)}")

# Save the enriched dataset
listings_df.to_csv("CRMLSListingswDistrict.csv")
sold_df.to_csv("CRMLSSoldwDistrict.csv")

#----------------------------------------------#
# January 2024 to June 2026 Data Cleaning Summary
#----------------------------------------------#
# Listings rows before cleaning: 967260
# Listings columns before cleaning: 88
# Sold rows before cleaning: 665439
# Sold columns before cleaning: 86
#----------------------------------------------#
### Illogical date field order: 
# Listings: 
# Flagged listing after close: 152
# Flagged purchase after close: 357
# Flagged negative timeline: 497
##
# Sold: 
# Flagged listing after close: 119
# Flagged purchase after close: 368
# Flagged negative timeline: 481
#----------------------------------------------#
### Invalid numeric values: 
# Listings: 
# Flagged Close Price: 13
# Flagged Living Area: 928
# Flagged Days on Market: 37
# Flagged Negative Rooms: 0
##
# Sold: 
# Flagged Close Price: 38
# Flagged Living Area: 538
# Flagged Days on Market: 64
# Flagged Negative Rooms: 0
#----------------------------------------------#
### Validate numeric dtypes: 
# Listings:
# AssociationFee: float64
# BathroomsTotalInteger: float64
# BedroomsTotal: float64
# ClosePrice: float64
# DaysOnMarket: int64
# GarageSpaces: float64
# Latitude: float64
# ListingKeyNumeric: int64
# ListPrice: float64
# LivingArea: float64
# Longitude: float64
# LotSizeAcres: float64
# LotSizeArea: float64
# LotSizeSquareFeet: float64
# MainLevelBedrooms: float64
# OriginalListPrice: float64
# ParkingTotal: float64
# Stories: float64
# StreetNumberNumeric: float64
# YearBuilt: float64
##
# Sold: 
# AssociationFee: float64
# BathroomsTotalInteger: float64
# BedroomsTotal: float64
# ClosePrice: float64
# DaysOnMarket: int64
# GarageSpaces: float64
# Latitude: float64
# ListingKeyNumeric: int64
# ListPrice: float64
# LivingArea: float64
# Longitude: float64
# LotSizeAcres: float64
# LotSizeArea: float64
# LotSizeSquareFeet: float64
# MainLevelBedrooms: float64
# OriginalListPrice: float64
# ParkingTotal: float64
# Stories: float64
# StreetNumberNumeric: float64
# YearBuilt: float64
#----------------------------------------------#
### Geographic Data Check: 
# Listings: 
# Missing Coordinates: 113438
# Flagged Null Coordinates: 112
# Out-of-bound Coordinates: 174
# Out-of-state Coordinates: 642
# Implausible Coordinates: 10
##
# Sold: 
# Missing Coordinates: 19698
# Flagged Null Coordinates: 57
# Out-of-bound Coordinates: 66
# Out-of-state Coordinates: 215
# Implausible Coordinates: 4
#----------------------------------------------#
# Listings rows after cleaning: 852686
# Listings columns after cleaning: 136
# Sold rows after cleaning: 645045
# Sold columns after cleaning: 132
import pandas as pd
import geopandas as gpd

# Import CRMLSListings and CRMLSSold CSVs
listings = pd.read_csv("C:/Users/izlal/IDXExchange_SU26/week2-3/CRMLSListingwRates.csv", low_memory = False)
sold = pd.read_csv("C:/Users/izlal/IDXExchange_SU26/week2-3/CRMLSSoldwRates.csv", low_memory = False)

# Before row count: 
print(f"Listings rows before cleaning: {len(listings)}")
print(f"Sold rows before cleaning: {len(sold)}")

# Convert date fields to datetime format (CloseDate, PurchaseContractDate, ListingContractDate, ContractStatusChangeDate)
date_fields = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']
for field in date_fields: 
    listings[field] = pd.to_datetime(listings[field], format = 'mixed')
    sold[field] = pd.to_datetime(sold[field], format = 'mixed')

# Data Consistency Check: 
# Validate the logical order of date fields: ListingContractDate should precede PurchaseContractDate, which should precede CloseDate. Create boolean flag columns to mark records that violate these rules:
print("Listings: ")
listings['listing_after_close_flag'] = listings['CloseDate'] < listings['ListingContractDate']
print(f"Flagged listing after close: {sum(listings['listing_after_close_flag'])}")
listings['purchase_after_close_flag'] = listings['CloseDate'] < listings['PurchaseContractDate']
print(f"Flagged purchase after close: {sum(listings['purchase_after_close_flag'])}")
listings['negative_timeline_flag'] = (listings['listing_after_close_flag'] | listings['purchase_after_close_flag'])
print(f"Flagged negative timeline: {sum(listings['negative_timeline_flag'])}")
listings = listings[~(listings['listing_after_close_flag']) & ~(listings['purchase_after_close_flag'])]

print("Sold: ")
sold['listing_after_close_flag'] = sold['CloseDate'] < sold['ListingContractDate']
print(f"Flagged listing after close: {sum(sold['listing_after_close_flag'])}")
sold['purchase_after_close_flag'] = sold['CloseDate'] < sold['PurchaseContractDate']
print(f"Flagged purchase after close: {sum(sold['purchase_after_close_flag'])}")
sold['negative_timeline_flag'] = (sold['listing_after_close_flag'] | sold['purchase_after_close_flag'])
print(f"Flagged negative timeline: {sum(sold['negative_timeline_flag'])}")
sold = sold[~(sold['listing_after_close_flag']) & ~(sold['purchase_after_close_flag'])]

# Remove or flag invalid numeric values: ClosePrice <= 0, LivingArea <= 0, DaysOnMarket < 0, negative Bedrooms or Bathrooms
print("Listings: ")
listings['closeprice_flag'] = (listings['ClosePrice'] <= 0)
print(f"Flagged Close Price: {sum(listings['closeprice_flag'])}")
listings['livingarea_flag'] = (listings['LivingArea'] <= 0)
print(f"Flagged Living Area: {sum(listings['livingarea_flag'])}")
listings['daysonmarket_flag'] = (listings['DaysOnMarket'] < 0)
print(f"Flagged Days on Market: {sum(listings['daysonmarket_flag'])}")
listings['neg_rooms_flag'] = (listings['BathroomsTotalInteger'] < 0) | (listings['BedroomsTotal'] < 0)
print(f"Flagged Negative Rooms: {sum(listings['neg_rooms_flag'])}")

print("Sold: ")
sold['closeprice_flag'] = (sold['ClosePrice'] <= 0)
print(f"Flagged Close Price: {sum(sold['closeprice_flag'])}")
sold['livingarea_flag'] = (sold['LivingArea'] <= 0)
print(f"Flagged Living Area: {sum(sold['livingarea_flag'])}")
sold['daysonmarket_flag'] = (sold['DaysOnMarket'] < 0)
print(f"Flagged Days on Market: {sum(listings['daysonmarket_flag'])}")
sold['neg_rooms_flag'] = (sold['BathroomsTotalInteger'] < 0) | (sold['BedroomsTotal'] < 0)
print(f"Flagged Negative Rooms: {sum(sold['neg_rooms_flag'])}")

# Remove unnecessary or redundant columns
# Handle missing values appropriately
### Week 5

# From Week 2:
# Flagged Missing Columns: ['WaterfrontYN', 'BasementYN', 'FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount', 'BuilderName', 'TaxYear', 'BuildingAreaTotal', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName', 'BelowGradeFinishedArea', 'BusinessType', 'CoveredSpaces', 'LotSizeDimensions', 'MiddleOrJuniorSchoolDistrict']

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
print(f"Listings missing coordinates: {sum(listings['missing_coords'])}")

sold['missing_coords'] = sold['Latitude'].isna() | sold['Longitude'].isna()
print(f"Sold missing coordinates: {sum(sold['missing_coords'])}")

# Flag Latitude = 0 or Longitude = 0 (sentinel null values)
listings['null_coords'] = (listings['Latitude'] == 0) | (listings['Longitude'] == 0)
print(f"Listings flagged null coordinates: {sum(listings['null_coords'])}")

sold['null_coords'] = (sold['Latitude'] == 0) | (sold['Longitude'] == 0)
print(f"Sold flagged null coordinates: {sum(sold['null_coords'])}")

# Flag Longitude > 0 errors (California coordinates should be negative)
listings['oob_coords'] = (listings['Longitude'] > 0)
print(f"Listings out of bound coordinates: {sum(listings['oob_coords'])}")

sold['oob_coords'] = (sold['Longitude'] > 0)
print(f"Sold out of bound coordinates: {sum(sold['oob_coords'])}")

### Week 5
# Flag out-of-state or implausible coordinates
# listings['oos_coords'] =
# listings['imp_coords'] = 

# Remove flagged rows: 
# listings = listings[~(listings['missing_coords']) & ~(listings['null_coords']) & ~(listings['oob_coords']) & ~(listings['oos_coords']) & ~(listings['imp_coords'])]
# sold = sold[~(sold['missing_coords']) & ~(sold['null_coords']) & ~(sold['oob_coords']) & ~(sold['oos_coords']) & ~(sold['imp_coords'])]

# After row counts: 
# print(f"Listings rows after cleaning: {len(listings)}")
# print(f"Sold rows after cleaning: {len(sold)}")

# # Add school district mapping
# # Read California school district boundary GeoJSON
# districts_gdf = gpd.read_file("C:/Users/izlal/IDXExchange_SU26/week4-5/DistrictAreas2526_-284845464123469011.geojson")

# # Filter the school district dataset to only include DistrictType == "Unified"
# districts_gdf = districts_gdf[districts_gdf["DistrictType"] == "Unified"]
# districts_gdf.head()

# districts_gdf = districts_gdf.to_crs(crs = "EPSG:4326")

# # Convert each property’s Latitude and Longitude into a geographic point
# listings_gdf = gpd.GeoDataFrame(listings, geometry = gpd.points_from_xy(listings["Longitude"], listings["Latitude"]), crs="EPSG:4326")
# sold_gdf = gpd.GeoDataFrame(sold, geometry = gpd.points_from_xy(sold["Longitude"], sold["Latitude"]), crs="EPSG:4326")

# # Perform a spatial join (gpd.sjoin) to determine which Unified School District polygon contains each property
# listings_joined = gpd.sjoin(listings_gdf, districts_gdf, how = "left", predicate = "within")
# sold_joined = gpd.sjoin(sold_gdf, districts_gdf, how = "left", predicate = "within")

# # Add the resulting DistrictName as a new column in your dataset
# listings_df = pd.DataFrame(listings_joined)
# sold_df = pd.DataFrame(sold_joined)

# # Save the enriched dataset
# listings_df.to_csv("CRMLSListingswDistrict.csv")
# sold_df.to_csv("CRMLSSoldwDistrict.csv")

###
# January 2024 to June 2026 Data Cleaning Summary
###
# Listings rows before cleaning: 967260
# Sold rows before cleaning: 665439
#----------------------------------------------#
### Illogical date field order: 
# Flagged listing after close: 152
# Flagged purchase after close: 357
# Flagged negative timeline: 497
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
# Flagged Days on Market: 37
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
# Listings missing coordinates: 113601
# Sold missing coordinates: 19789
# Listings flagged null coordinates: 112
# Sold flagged null coordinates: 57
# Listings out of bound coordinates: 174
# Sold out of bound coordinates: 66
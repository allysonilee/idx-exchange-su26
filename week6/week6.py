import pandas as pd
import geopandas as gpd

# Import relevant CRMLSListing and CRMLSSold CSVs
listings = pd.read_csv("CSVs/CRMLSListingClean.csv", low_memory = False)
sold = pd.read_csv("CSVs/CRMLSSoldClean.csv", low_memory = False)

# Convert date fields to datetime format (CloseDate, PurchaseContractDate, ListingContractDate, ContractStatusChangeDate)
date_fields = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']
for field in date_fields: 
    listings[field] = pd.to_datetime(listings[field], format = 'mixed')
    sold[field] = pd.to_datetime(sold[field], format = 'mixed')

### Add market metrics
# Price Ratio = ClosePrice/OriginalListPrice
listings['price_ratio'] = listings['ClosePrice']/listings['OriginalListPrice']
sold['price_ratio'] = sold['ClosePrice']/sold['OriginalListPrice']

# Close to Original List Ratio = ClosePrice/OriginalListPrice
listings['close_to_original_list_ratio'] = listings['ClosePrice']/listings['OriginalListPrice']
sold['close_to_original_list_ratio'] = sold['ClosePrice']/sold['OriginalListPrice']

# Price Per Sq Ft = ClosePrice/LivingArea
listings['PPSF'] = listings['ClosePrice']/listings['LivingArea']
sold['PPSF'] = sold['ClosePrice']/sold['LivingArea']

# Days On Market = DaysOnMarket
listings['days_on_market'] = listings['DaysOnMarket']
sold['days_on_market'] = sold['DaysOnMarket']

# Year / Month / YrMo = derived from CloseDate
listings['YrMo'] = listings['CloseDate'].dt.strftime('%Y-%m')
sold['YrMo'] = sold['CloseDate'].dt.strftime('%Y-%m')

# Listing to Contract Days = PurchaseContractDate - ListingContractDate
listings['listing_to_contract_days'] = listings['PurchaseContractDate'] - listings['ListingContractDate']
sold['listing_to_contract_days'] = sold['PurchaseContractDate'] - sold['ListingContractDate']

# Contract to Close Days = CloseDate - PurchaseContractDate
listings['contract_to_close_days'] = listings['CloseDate'] - listings['PurchaseContractDate']
sold['contract_to_close_days'] = sold['CloseDate'] - sold['PurchaseContractDate']

# Sample output table with new columns
print("Sold sample of engineered metrics: ")
print(sold[['ListingKey', 'ClosePrice', 'OriginalListPrice', 'LivingArea', 'price_ratio', 'close_to_original_list_ratio', 'PPSF', 'days_on_market', 'YrMo', 'listing_to_contract_days', 'contract_to_close_days']].head(5))

### Add school district mapping
# Read California school district boundary GeoJSON
districts_gdf = gpd.read_file("week6/DistrictAreas2526_-284845464123469011.geojson")

# Filter the school district dataset to only include DistrictType == "Unified"
districts_gdf = districts_gdf[districts_gdf["DistrictType"] == "Unified"]
districts_gdf.head()

districts_gdf = districts_gdf.to_crs(crs = "EPSG:4326")

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

### Segment Analysis
# After creating your engineered metrics, group the analysis by key dimensions to uncover market patterns.
# Aggregate metrics based on columns
agg_metrics = {'ClosePrice': ['median', 'mean', 'std'],  
               'price_ratio': ['median', 'mean'], 
               'PPSF': ['median', 'mean'], 
               'close_to_original_list_ratio': ['mean'], 
               'days_on_market': ['median', 'mean'], 
               'listing_to_contract_days': ['median'], 
               'contract_to_close_days': ['median'], 
               'ListingKey': 'count', 
               'LivingArea': ['median'], 
               'ListPrice': ['median']}

# Generate summary statistics for each segment:
# • PropertyType and PropertySubType
list_by_property = listings_df.groupby(['PropertyType', 'PropertySubType']).agg(agg_metrics)
sold_by_property = sold_df.groupby(['PropertyType', 'PropertySubType']).agg(agg_metrics)

# • CountyOrParish and MLSAreaMajor
list_by_geo = listings_df.groupby(['CountyOrParish', 'MLSAreaMajor']).agg(agg_metrics)
sold_by_geo = sold_df.groupby(['CountyOrParish', 'MLSAreaMajor']).agg(agg_metrics)

# • ListOfficeName and BuyerOfficeName (for competitive intelligence)
list_by_office = listings_df.groupby(['ListOfficeName', 'BuyerOfficeName']).agg(agg_metrics)
sold_by_office = sold_df.groupby(['ListOfficeName', 'BuyerOfficeName']).agg(agg_metrics)

# Sample segmented summary table grouped by CountyOrParish
print("Segmented Summary - Sold by CountyOrParish/MLSAreaMajor: ")
print(sold_by_geo.head(5))

# Save the enriched dataset
listings_df.to_csv("CSVs/CRMLSListingwDistrict.csv", index = False)
sold_df.to_csv("CSVs/CRMLSSoldwDistrict.csv", index = False)

#------------------------------------------------------------#
# Sold sample of engineered metrics:
#------------------------------------------------------------#
#    ListingKey  ClosePrice  OriginalListPrice  ...     YrMo  listing_to_contract_days  contract_to_close_days
# 0   535486633       950.0                0.0  ...  2024-01                  901 days                  0 days
# 1   529986282     45000.0            75000.0  ...  2024-01                  887 days                 25 days
# 2   529618166    141500.0           199000.0  ...  2024-01                  832 days                 76 days
# 3   522614340     15000.0            19500.0  ...  2024-01                  809 days                145 days
# 4   518662094      1200.0             5500.0  ...  2024-01                 1004 days                  0 days

# [5 rows x 11 columns]

#------------------------------------------------------------#
# Segmented Summary - Sold by CountyOrParish/MLSAreaMajor:
#------------------------------------------------------------#
#                                                          ClosePrice                ... LivingArea  ListPrice
#                                                              median          mean  ...     median     median
# CountyOrParish MLSAreaMajor                                                        ...                      
# Alameda        699 - Not Defined                          1057500.0  1.172296e+06  ...     1529.0   999000.0
#                BERK - Berkeley                             786499.5  9.043915e+05  ...     1244.5   708750.0
#                GLV - Glenview                             1400000.0  1.400000e+06  ...     4088.0  1395000.0
#                Missing                                    1050000.0  1.265519e+06  ...     1583.0   995000.0
#                RO - Compton S of Rosecrans, E of Alameda  1125000.0  1.125000e+06  ...     1583.0  1199000.0

# [5 rows x 15 columns]
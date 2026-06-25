import pandas as pd
import os
import glob

listing = "C:/Users/izlal/IDXExchange_SU26/CRMLSListing"
listing_files = glob.glob(os.path.join(listing, "CRMLSListing*.csv"))
listing_dfs = [pd.read_csv(listing_file, low_memory = False) for listing_file in listing_files]

list_rows_before_concat = sum(len(df) for df in listing_dfs)
print("Listings before concatenation: ", list_rows_before_concat)

listing_df = pd.concat(listing_dfs)

list_rows_after_concat = len(listing_df)
print("Listings after concatenation: ", list_rows_after_concat)

list_rows_before_filter = len(listing_df)
print("Listings before Residential filter: ", list_rows_before_filter)

listing_df = listing_df[listing_df["PropertyType"] == "Residential"]

list_rows_after_filter = len(listing_df)
print("Listings after Residential filter: ", list_rows_after_filter)

listing_df.to_csv("ConcatenatedCRMLSListing.csv")

sold = "C:/Users/izlal/IDXExchange_SU26/CRMLSSold"
sold_files = glob.glob(os.path.join(sold, "CRMLSSold*.csv"))
sold_dfs = [pd.read_csv(sold_file, low_memory = False) for sold_file in sold_files]

sold_rows_before_concat = sum(len(df) for df in sold_dfs)
print("Sold before concatenation: ", sold_rows_before_concat)

sold_df = pd.concat(sold_dfs)

sold_rows_after_concat = len(sold_df)
print("Sold after concatenation: ", sold_rows_after_concat)

sold_rows_before_filter = len(sold_df)
print("Sold before Residential filter: ", sold_rows_before_filter)

sold_df = sold_df[sold_df["PropertyType"] == "Residential"]

sold_rows_after_filter = len(sold_df)
print("Sold after Residential filter: ", sold_rows_after_filter)

sold_df.to_csv("ConcatenatedCRMLSSold.csv")
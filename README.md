# IDX Exchange - Data Analyst Internship (Summer 2026)
## About
Analyze real-world MLS transaction data through weekly deliverables over a 12 week program. 
Each heading corresponds to a unique module's folder including .py file(s) with dataset cleaning scripts. 
Datasets are stored in a particular CSV folder (untracked on GitHub). 
## Week 1
Retrieve and respectively concatenate CRMLS sold and listing data from January 2024 to the most recently complete calendar month from the CSV folder. 
Save the concatenated dataset consisting of exclusively residential property types in the CSV folder. 
## Week 2-3
### Week 2
Inspect the sold data and filter to only include relevant property records by removing columns with high amounts of missing data. 
Save the filtered data as a new CSV in the CSV folder.
### Week 3
Merge the concatenated sold and listing datasets with the FRED MORTGAGE30US series on a monthly key to gauge mortgage rates for each sold and listed property based on month. 
Save the enriched datasets as new CSVs in the CSV folder. 
## Week 4-5
Transform data in the sold and listed dataframe columns to their correct datatypes. 
Remove unnecessary and redundant columns. 
Appropriately impute missing values. 
Flag and remove invalid numeric values and illogical date order fields. 
Flag and remove missing, out-of-state, and implausible coordinates. 
Save the cleaned datasets as new CSVs in the CSV folder. 

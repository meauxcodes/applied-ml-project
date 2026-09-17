import pandas as pd

raw_data = pd.read_csv("../data/raw/sam_garmin_data.csv")

print(raw_data.info())
print(raw_data.isna().sum())
# SpO2 data is missing for the first 8 days of data collection since the 
# setting wasn't turned on in the watch system. That data will be captured 
# in it's own dataset and dropped from the main data set. This is done to
# preserve it for a future SpO2-specific dataset once more post-9/12 data exists

spo2_cols = ["date","avg SpO2", "lowest SpO2", "7 day avg SpO2", "avg sleep SpO2"]
spo2_data = raw_data[spo2_cols]

# remove SpO2 data from main data set
main_data = raw_data.drop(columns=["avg SpO2", "lowest SpO2", "7 day avg SpO2", "avg sleep SpO2"])

# double check SpO2 data is removed
print(main_data.isna().sum())

# SpO2 data is gone, now to address missing HRV data
# Since HRV weekly average needed some time to calculate,
# the first instance of a weekly average will be backfilled 
# into the missing cells. The data wasn't missing, just wasn't 
# enough data to calculate it yet so backfilling seems 
# reasonable in this case

main_data["hrv weekly avg"] = main_data["hrv weekly avg"].bfill()
print(main_data["hrv weekly avg"])

# double check for any remaining missing values
print(main_data.isna().sum())

# scan for outliers and incorrect values
print(main_data.describe().T)

# noticed some small data points (resting calories) 
# due to a partial day reading pull. Moving to drop 
# the most recent day to avoid partial-day data

main_data = main_data.iloc[:-1]

### OTHER CLEANING COMMENTS###
#   Remaining outliers (i.e. low REM % on 9/5, elevated heart
#   rate/stress on other nights) were reviewed individually and
#   kept rather than removed. They reflect real recorded nights
#   tied to known factors (late nights, lifestyle
#   factors like alcohol use, child interruptions) rather than data collection errors.

main_data.to_csv("../data/clean/cleaned_garmin_data.csv",index = False)
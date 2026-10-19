import pandas as pd

pd.set_option("display.width", 200)

raw = pd.read_csv("../data/raw/cohort_joined.csv")
print(raw.shape)
print("participants:", raw["participant_id"].nunique())
print(raw["cohort"].value_counts())
print(raw.describe().T)

cleaned = raw.copy()
print("blank in any column:", cleaned.isna().any(axis=1).sum())
print("avg stress below 0:", (cleaned["averageStressInStressLevel"] < 0).sum())
print("HRV 5-min high of 0:", (cleaned["lastNight5MinHigh"] == 0).sum())
print("sleep under 30 minutes:", (cleaned["durationInMs"] < 0.5 * 3600000).sum())
print("sleep under 1 hour:", (cleaned["durationInMs"] < 1 * 3600000).sum())
print("sleep under 2 hours:", (cleaned["durationInMs"] < 2 * 3600000).sum())
print("sleep under 3 hours:", (cleaned["durationInMs"] < 3 * 3600000).sum())
print("zero steps:", (cleaned["steps"] == 0).sum())
print("resting calories under 1000:", (cleaned["bmrKilocalories"] < 1000).sum())
print("steps over 40000:", (cleaned["steps"] > 40000).sum())

### SPLIT THE DATASET INTO with and without SPO2 data

dataset_with_spo2 = cleaned
# 
pulse_ox_features = [
    "spo2_mean", 
    "spo2_std", 
    "spo2_min", 
    "spo2_max"
]

dataset_without_spo2 = cleaned.drop(columns = pulse_ox_features)

#remove rows with blank values
dataset_without_spo2 = dataset_without_spo2.dropna()
print("dataset without spo2 after dropping blanks:", dataset_without_spo2.shape)
dataset_with_spo2 = dataset_with_spo2.dropna()
print("dataset with spo2 after dropping blanks:", dataset_with_spo2.shape)

#my methodology for cleaning this data is to only remove data that is impossible
#only keep the rows where the average stress is real (above 0)
dataset_without_spo2 = dataset_without_spo2[dataset_without_spo2["averageStressInStressLevel"] > 0]
print("dataset without spo2 after dropping negative stress:", dataset_without_spo2.shape)
dataset_with_spo2 = dataset_with_spo2[dataset_with_spo2["averageStressInStressLevel"] > 0]
print("dataset with spo2 after dropping negative stress:", dataset_with_spo2.shape)

#only keep rows where HRV is real

dataset_without_spo2 = dataset_without_spo2[dataset_without_spo2["lastNight5MinHigh"] > 0]
print("dataset without spo2 after removing invalid HRV:", dataset_without_spo2.shape)
dataset_with_spo2 = dataset_with_spo2[dataset_with_spo2["lastNight5MinHigh"] > 0]
print("dataset with spo2 after removing invalid HRV:", dataset_with_spo2.shape)

#only keep rows where the watch was worn a full day (resting calories 1,000 or more)
dataset_without_spo2 = dataset_without_spo2[dataset_without_spo2["bmrKilocalories"] >= 1000]
print("dataset without spo2 after removing partial days:", dataset_without_spo2.shape)
dataset_with_spo2 = dataset_with_spo2[dataset_with_spo2["bmrKilocalories"] >= 1000]
print("dataset with spo2 after removing partial days:", dataset_with_spo2.shape)

# 5. keep rows where daytime steps were recorded (above 0)
dataset_without_spo2 = dataset_without_spo2[dataset_without_spo2["steps"] > 0]
print("dataset without spo2 after removing zero-step days:", dataset_without_spo2.shape)
dataset_with_spo2 = dataset_with_spo2[dataset_with_spo2["steps"] > 0]
print("dataset with spo2 after removing zero-step days:", dataset_with_spo2.shape)

dataset_without_spo2.to_csv("../data/clean/dataset_without_spo2_cleaned.csv", index=False)
print("Dataset Without SPO2 Saved")
print("The number of participants is:", dataset_without_spo2.nunique())
print("The original data has been transformed from", raw.shape, "to", dataset_without_spo2.shape, "losing only", raw.shape[0] - dataset_without_spo2.shape[0], "rows", "or", round((raw.shape[0] - dataset_without_spo2.shape[0]) / raw.shape[0] * 100, 2), "% of the original data.")


dataset_with_spo2.to_csv("../data/clean/dataset_with_spo2_cleaned.csv", index=False)
print("Dataset With SPO2 Saved")
print("The number of participants is:", dataset_with_spo2.nunique())
print("The original data has been transformed from", raw.shape, "to", dataset_with_spo2.shape, "losing only", raw.shape[0] - dataset_with_spo2.shape[0], "rows", "or", round((raw.shape[0] - dataset_with_spo2.shape[0]) / raw.shape[0] * 100, 2), "% of the original data.")


data_dictionary = {
    "participant_id": ["Anonymous code for each participant", "text"],
    "calendarDate": ["Date Garmin assigns to the record", "date"],
    "cohort": ["Generic label for the participant's program group", "text"],
    "durationInMs": ["Total time asleep, not counting awake time", "milliseconds"],
    "deepSleepDurationInMs": ["Time in deep sleep", "milliseconds"],
    "lightSleepDurationInMs": ["Time in light sleep", "milliseconds"],
    "remSleepInMs": ["Time in REM sleep", "milliseconds"],
    "awakeDurationInMs": ["Time awake during the sleep period", "milliseconds"],
    "overallSleepScore": ["Garmin's overall rating of the night", "score 0 to 100"],
    "lastNightAvg": ["Average heart rate variability across the night", "milliseconds"],
    "lastNight5MinHigh": ["Highest 5-minute average heart rate variability in the night", "milliseconds"],
    "restingHeartRateInBeatsPerMinute": ["Resting heart rate for the day", "beats per minute"],
    "minHeartRateInBeatsPerMinute": ["Lowest heart rate recorded that day", "beats per minute"],
    "maxHeartRateInBeatsPerMinute": ["Highest heart rate recorded that day", "beats per minute"],
    "averageStressInStressLevel": ["Average Garmin stress score across the day", "score 0 to 100"],
    "maxStressInStressLevel": ["Highest stress score recorded that day", "score 0 to 100"],
    "steps": ["Total steps for the day", "count"],
    "activeKilocalories": ["Calories burned through activity", "kilocalories"],
    "bmrKilocalories": ["Calories burned at rest", "kilocalories"],
    "moderateIntensityDurationInMs": ["Time in moderate-intensity activity", "milliseconds"],
    "vigorousIntensityDurationInMs": ["Time in vigorous-intensity activity", "milliseconds"],
    "breathsPerMinute_mean": ["Average breathing rate during sleep","breaths per minute"],
    "breathsPerMinute_std": ["How much breathing varied during sleep","breaths per minute"],
    "breathsPerMinute_min": ["Lowest breathing rate during sleep","breaths per minute"],
    "breathsPerMinute_max": ["Highest breathing rate during sleep","breaths per minute"],
    "spo2_mean":["Average nightly SpO2 value","% SpO2"],
    "spo2_std":["How much blood oxygen content varied during sleep","% points"],
    "spo2_min":["Minimum nightly SpO2 value","% SpO2"],
    "spo2_max":["Maximum nightly SpO2 value","% SpO2"]
}

# build one row per column in the cleaned table
rows = []
for column in cleaned.columns:
    meaning = data_dictionary[column][0]
    unit = data_dictionary[column][1]
    rows.append([column, meaning, unit])

dictionary_table = pd.DataFrame(rows, columns=["column", "meaning", "unit"])
dictionary_table.to_csv("../data/clean/cohort_data_dictionary.csv", index=False)
print(dictionary_table)
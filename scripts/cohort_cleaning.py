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

#remove rows with blank values
cleaned = cleaned.dropna()
print("after dropping blanks:", cleaned.shape)

#my methodology for cleaning this data is to only remove data that is impossible
#only keep the rows where the average stress is real (above 0)
cleaned = cleaned[cleaned["averageStressInStressLevel"] > 0]
print("after dropping negative stress:", cleaned.shape)

#only keep rows where HRV is real

cleaned = cleaned[cleaned["lastNight5MinHigh"] > 0]
print("after removing invalid HRV:", cleaned.shape)

#only keep rows where the watch was worn a full day (resting calories 1,000 or more)
cleaned = cleaned[cleaned["bmrKilocalories"] >= 1000]
print("after removing partial days:", cleaned.shape)

# 5. keep rows where daytime steps were recorded (above 0)
cleaned = cleaned[cleaned["steps"] > 0]
print("after removing zero-step days:", cleaned.shape)

cleaned.to_csv("../data/clean/cohort_cleaned.csv", index=False)
print("Saved")
print("The original data has been transformed from", raw.shape, "to", cleaned.shape, "losing only", raw.shape[0] - cleaned.shape[0], "rows", "or", round((raw.shape[0] - cleaned.shape[0]) / raw.shape[0] * 100, 2), "% of the original data.")


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
    "breathsPerMinute_mean": ["Average breating rate during sleep","breaths per minute"],
    "breathsPerMinute_std": ["How much breathing varied during sleep","breaths per minute"],
    "breathsPerMinute_min": ["Lowest breating rate during sleep","breaths per minute"],
    "breathsPerMinute_max": ["Highest breating rate during sleep","breaths per minute"],
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
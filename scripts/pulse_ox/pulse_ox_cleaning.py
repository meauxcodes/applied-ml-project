import pandas as pd

pd.set_option("display.width", 200)

raw = pd.read_csv("../../data/raw/pulse_ox_joined.csv")
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

cleaned.to_csv("../../data/clean/pulse_ox_cleaned.csv", index=False)
print("Saved")
print("The original data has been transformed from", raw.shape, "to", cleaned.shape, "losing only", raw.shape[0] - cleaned.shape[0], "rows", "or", round((raw.shape[0] - cleaned.shape[0]) / raw.shape[0] * 100, 2), "% of the original data.")



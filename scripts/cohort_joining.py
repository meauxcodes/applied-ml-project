from pathlib import Path
import pandas as pd

cohort_labels = {
    "Sleep Savant Since Feb 24": "cohort_01",
    "Sleep Savant Since Mar 19": "cohort_02",
    "Sleep Savant Since May 24": "cohort_03",
    "Sleep Savant Since Sep 8": "cohort_04",
    "Sleep Savant Since Nov 9": "cohort_05",
    "Sleep Savant Since Jan 24": "cohort_06",
    "Sleep Savant Since Apr 14": "cohort_07",
    "Sleep Savant Since Jun 29": "cohort_08",
}

stacked_dir = Path("/Volumes/ROG Strix/eventide_data/cohort_stacked")

sleep = pd.read_csv(stacked_dir / "garmin-connect-sleep-summary.csv")
print("sleep", sleep.shape)

hrv = pd.read_csv(stacked_dir / "garmin-connect-hrv-summary.csv")
print("hrv", hrv.shape)

daily = pd.read_csv(stacked_dir / "garmin-connect-daily-summary.csv")
print("daily", daily.shape)

keys = ["participant_id", "calendarDate"]

sleep = sleep[keys + ["cohort", "durationInMs", "deepSleepDurationInMs", "lightSleepDurationInMs", "remSleepInMs", "awakeDurationInMs", "overallSleepScore"]]
sleep = sleep.drop_duplicates(subset=keys, keep="last")
print("sleep after", sleep.shape)

hrv = hrv[keys + ["lastNightAvg", "lastNight5MinHigh"]]
hrv = hrv.drop_duplicates(subset=keys, keep="last")
print("hrv after", hrv.shape)

daily = daily[keys + ["restingHeartRateInBeatsPerMinute", "minHeartRateInBeatsPerMinute",
                      "maxHeartRateInBeatsPerMinute", "averageStressInStressLevel",
                      "maxStressInStressLevel", "steps", "activeKilocalories", "bmrKilocalories",
                      "moderateIntensityDurationInMs", "vigorousIntensityDurationInMs"]]
daily = daily.drop_duplicates(subset=keys, keep="last")
print("daily after", daily.shape)



#98 unique participants across 8 cohorts, 28 of them enrolled twice, duplicate days removed.

merged = sleep.merge(hrv, on=keys, how="inner")
print("sleep + hrv", merged.shape)

merged = merged.merge(daily, on=keys, how="inner")
print("sleep + hrv + daily", merged.shape)

print(merged.head())

print(merged.isna().sum())

# build a lookup: real ID -> anonymous code
id_lookup = {}
number = 1
for real_id in merged["participant_id"].unique():
    id_lookup[real_id] = "P" + str(number)
    number = number + 1

# apply the lookup
merged["participant_id"] = merged["participant_id"].replace(id_lookup)

# swap cohort folder names for generic labels
merged["cohort"] = merged["cohort"].str.strip().replace(cohort_labels)

merged.to_csv("../data/raw/cohort_joined.csv", index=False)
print(merged.head())
print(merged.shape)
print("saved")
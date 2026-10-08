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

stacked_dir = Path("/Volumes/ROG Strix/eventide_data/cohort_stacked/pulse_ox")

sleep = pd.read_csv(stacked_dir / "garmin-connect-sleep-summary.csv")
print("sleep", sleep.shape)

nightly_respiration = pd.read_csv(stacked_dir / "sleep_respiration.csv")
print("sleep respiration", nightly_respiration.shape)

sleep_pulse_ox = pd.read_csv(stacked_dir / "sleep_pulse_ox.csv")
print("sleep pulse ox", sleep_pulse_ox.shape)

hrv = pd.read_csv(stacked_dir / "garmin-connect-hrv-summary.csv")
print("hrv", hrv.shape)

daily = pd.read_csv(stacked_dir / "garmin-connect-daily-summary.csv")
print("daily", daily.shape)

keys = ["participant_id", "calendarDate"]
night_keys = ["participant_id", "sleepSummaryId"]

sleep = sleep[keys + ["cohort", "durationInMs", "deepSleepDurationInMs", "lightSleepDurationInMs", "remSleepInMs", "awakeDurationInMs", "overallSleepScore","sleepSummaryId"]]
sleep = sleep.drop_duplicates(subset=keys, keep="last")
print("sleep after", sleep.shape)

nightly_respiration = nightly_respiration[night_keys + ["breathsPerMinute_mean","breathsPerMinute_std", "breathsPerMinute_min", "breathsPerMinute_max"]]

sleep_pulse_ox = sleep_pulse_ox[night_keys + ["spo2_mean", "spo2_std", "spo2_min", "spo2_max"]]

hrv = hrv[keys + ["lastNightAvg", "lastNight5MinHigh"]]
hrv = hrv.drop_duplicates(subset=keys, keep="last")
print("hrv after", hrv.shape)

daily = daily.drop_duplicates(subset=keys, keep="last")

# heart rate lows are measured overnight, so they keep their date
daily_night = daily[keys + ["restingHeartRateInBeatsPerMinute", "minHeartRateInBeatsPerMinute"]]
# activity and stress describe the daytime, so move them forward one date.
# that lines each day up with the night that followed it
daily_before = daily[keys + ["maxHeartRateInBeatsPerMinute", "averageStressInStressLevel",
                             "maxStressInStressLevel", "steps", "activeKilocalories",
                             "bmrKilocalories", "moderateIntensityDurationInMs",
                             "vigorousIntensityDurationInMs"]].copy()
next_date = pd.to_datetime(daily_before["calendarDate"]) + pd.Timedelta(days=1)
daily_before["calendarDate"] = next_date.dt.strftime("%Y-%m-%d")
print("daily after", daily.shape)



#98 unique participants across 8 cohorts, 28 of them enrolled twice, duplicate days removed.

merged = sleep.merge(nightly_respiration, on=night_keys, how="inner")
print("sleep + nightly respiration", merged.shape)

merged = merged.merge(sleep_pulse_ox, on = night_keys, how = "inner")
print("sleep + nightly respiration + sleep pulse ox")

merged = merged.merge(hrv, on=keys, how="inner")
print("sleep + nightly respiration + sleep pulse ox + hrv", merged.shape)



merged = merged.merge(daily_night, on=keys, how="inner")
merged = merged.merge(daily_before, on=keys, how="inner")
print("sleep + nightly respiration + sleep pulse ox + hrv + daily", merged.shape)

merged = merged.drop(columns = ["sleepSummaryId"])

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


merged.to_csv("../../data/raw/pulse_ox_joined.csv", index=False)
print(merged.head())
print(merged.shape)
print("saved")
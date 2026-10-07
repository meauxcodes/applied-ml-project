import pandas as pd
from pathlib import Path

stacked_dir = Path("/Volumes/ROG Strix/eventide_data/cohort_stacked")
sleep_respiration = pd.read_csv(stacked_dir / "garmin-connect-sleep-respiration.csv")
print(sleep_respiration.shape, sleep_respiration.head())
print(sleep_respiration["breathsPerMinute"].describe())
print(sum(sleep_respiration["breathsPerMinute"] <=0))

sleep_respiration = sleep_respiration[sleep_respiration["breathsPerMinute"] > 0]
print(sleep_respiration["breathsPerMinute"].describe())
print(sum(sleep_respiration["breathsPerMinute"] <=0))

print(sleep_respiration.shape)
keys = ["participant_id", "sleepSummaryId", "unixTimestampInMs"]
sleep_respiration = sleep_respiration.drop_duplicates(subset=keys, keep="last")
print(sleep_respiration.shape)

sleep_respiration = sleep_respiration.groupby(["participant_id", "sleepSummaryId"])["breathsPerMinute"].agg(["mean", "std", "min", "max", "count"]).reset_index().rename(columns={"mean": "breathsPerMinute_mean", "std": "breathsPerMinute_std", "min": "breathsPerMinute_min", "max": "breathsPerMinute_max", "count": "breathsPerMinute_count"})
print(sleep_respiration.head(),sleep_respiration.describe())

sleep_respiration.to_csv(stacked_dir / "sleep_respiration.csv", index = False)
sleep_respiration.to_csv(stacked_dir / "pulse_ox/sleep_respiration.csv", index = False)
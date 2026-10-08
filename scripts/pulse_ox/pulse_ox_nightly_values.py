import pandas as pd
from pathlib import Path

stacked_dir = Path("/Volumes/ROG Strix/eventide_data/cohort_stacked/pulse_ox")
sleep_pulse_ox = pd.read_csv(stacked_dir / "garmin-connect-sleep-pulse-ox.csv")
print(sleep_pulse_ox.shape, sleep_pulse_ox.head())
print(sleep_pulse_ox["spo2"].describe())

print(sleep_pulse_ox.shape)
keys = ["participant_id", "sleepSummaryId", "unixTimestampInMs"]
sleep_pulse_ox = sleep_pulse_ox.drop_duplicates(subset=keys, keep="last")
print(sleep_pulse_ox.shape)

sleep_pulse_ox = sleep_pulse_ox.groupby(["participant_id", "sleepSummaryId"])["spo2"].agg(["mean", "std", "min", "max"]).reset_index().rename(columns={"mean": "spo2_mean", "std": "spo2_std", "min": "spo2_min", "max": "spo2_max"})
print(sleep_pulse_ox.head(),sleep_pulse_ox.describe())

sleep_pulse_ox.to_csv(stacked_dir / "sleep_pulse_ox.csv", index = False)



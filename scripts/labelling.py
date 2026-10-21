import pandas as pd

dataset_with_spo2 = pd.read_csv("../data/clean/dataset_with_spo2_cleaned.csv")
dataset_without_spo2 = pd.read_csv("../data/clean/dataset_without_spo2_cleaned.csv")

### Label low recovery nights
dataset_without_spo2["hrv_personal_average"] = dataset_without_spo2.groupby("participant_id")["lastNightAvg"].transform("mean")
dataset_without_spo2["hrv_ratio"] = dataset_without_spo2["lastNightAvg"]/dataset_without_spo2["hrv_personal_average"]
dataset_without_spo2["low_recovery"] = dataset_without_spo2["hrv_ratio"]<=.8

### Label low oxygen nights
dataset_with_spo2["spo2_z"] = (dataset_with_spo2["spo2_mean"]-dataset_with_spo2["spo2_mean"].mean())/dataset_with_spo2["spo2_mean"].std()
dataset_with_spo2["low_oxygen"] = dataset_with_spo2["spo2_z"]<=-1

### Remove the answer key (low recovery)

nb_answer_key = [
    "hrv_personal_average",
    "lastNightAvg",
    "lastNight5MinHigh",
    "hrv_ratio"
]
print(f"Percent of nights where hrv is at or below 20% of an individual's normal: {((dataset_without_spo2["hrv_ratio"]<=.8).sum()/len(dataset_without_spo2)*100).round(3)}%")
dataset_without_spo2 = dataset_without_spo2.drop(columns = nb_answer_key)
dataset_without_spo2.to_csv("../data/clean/nb_labeled.csv", index = False)

### Remove the answer key (low oxygen)

dt_answer_key = [
    "spo2_z",
    "spo2_mean",
    "spo2_min",
    "spo2_max",
    "spo2_std"
]
print(f"Percent of nights where spo2 is at or below -1 z: {((dataset_with_spo2["spo2_z"]<=-1).sum()/len(dataset_with_spo2)*100).round(3)}%")
dataset_with_spo2 = dataset_with_spo2.drop(columns = dt_answer_key)
dataset_with_spo2.to_csv("../data/clean/dt_labeled.csv", index = False)

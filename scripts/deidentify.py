from pathlib import Path
import pandas as pd

joined = Path("/Volumes/ROG Strix/school/eventide_data")

cohort_joined = pd.read_csv(joined/ "cohort_joined.csv")
print("joined", cohort_joined.shape)

cohort_joined = cohort_joined.sort_values(by = "participant_id")
# build a lookup: real ID -> anonymous code
id_lookup = {}
number = 1
for real_id in cohort_joined["participant_id"].unique():
    id_lookup[real_id] = "P" + str(number)
    number = number + 1

# apply the lookup
cohort_joined["participant_id"] = cohort_joined["participant_id"].replace(id_lookup)


cohort_joined.to_csv("../data/raw/cohort_joined.csv", index=False)
print(cohort_joined.head())
print(cohort_joined.shape)
print("saved")
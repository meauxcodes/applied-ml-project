from pathlib import Path
import pandas as pd


cohort_exports_dir = Path("/Volumes/ROG Strix/eventide_data/cohort_exports")

wanted_data_types = [
    #"questionnaire",
    "garmin-connect-sleep-summary",##
    "garmin-connect-sleep-stage", ##
    "garmin-connect-hrv-summary", ##
    "garmin-connect-stress",##
    "garmin-connect-respiration",
    "garmin-connect-sleep-respiration",
    #"garmin-connect-pulse-ox",
    #"garmin-connect-sleep-pulse-ox",
    "garmin-connect-daily-summary", ##
    "garmin-connect-user-metrics",
]

# NEW: one empty list per data type, made once, before any loop
tables = {}
for name in wanted_data_types:
    tables[name] = []

count = 0
dropped = 0

for cohort_dir in cohort_exports_dir.iterdir():
    if not cohort_dir.is_dir(): continue
    for cohort_subdir in cohort_dir.iterdir():
        if not cohort_subdir.is_dir(): continue
        for participant in cohort_subdir.iterdir():
            if not participant.is_dir(): continue
            for data_type in participant.iterdir():
                if data_type.name in wanted_data_types:
                    for data_file in data_type.iterdir():
                        if not data_file.is_file(): continue
                        if data_file.suffix != ".csv": continue      # NEW: skips .DS_Store etc.
                        try:
                            df = pd.read_csv(data_file, skiprows=5)
                        except pd.errors.EmptyDataError:
                            dropped += 1
                            continue

                        df["participant_id"] = participant.name      # NEW: who this row belongs to
                        df["cohort"] = cohort_subdir.name               # NEW: which cohort
                        tables[data_type.name].append(df)            # NEW: file it in the right bin
                        count += 1

# NEW: sanity check after everything is read
print("files read:", count, "| dropped:", dropped)
for name in tables:
    print(name, len(tables[name]))

output_dir = Path("/Volumes/ROG Strix/eventide_data/cohort_stacked")
output_dir.mkdir(parents=True, exist_ok=True)      # make the folder if it isn't there

for name in tables:
    if len(tables[name]) == 0:                     # skip data types we didn't read
        continue
    stacked = pd.concat(tables[name], ignore_index=True)    # stack the list into one table
    stacked.to_csv(output_dir / f"{name}.csv", index=False) # save it
    print(name, stacked.shape)                     # (rows, columns)
    print(list(stacked.columns))

                    

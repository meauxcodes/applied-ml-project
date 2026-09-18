import wfdb

# Option A: Download an entire database to your local folder
# (e.g., 'apnea-ecg' or 'mmash')
wfdb.dl_database("apnea-ecg", dl_dir="../data/raw/apnea-ecg")

# Option B: Stream a specific record directly into memory
# record = wfdb.rdrecord('a01', pn_dir='apnea-ecg')
# annotation = wfdb.rdann('a01', 'apnea', pn_dir='apnea-ecg')
# print("Signals:", record.p_signals.shape)
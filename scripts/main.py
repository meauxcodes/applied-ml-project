import subprocess
import sys

scripts = [
    "cohort_stacking.py",
    "cohort_respiration.py",
    "pulse_ox/pulse_ox_nightly_values.py",
    "cohort_joining.py",
    "deidentify.py",
    "cohort_cleaning.py",
]

for script in scripts:
    result = subprocess.run(["python", script])
    if result.returncode != 0:
        print(f"Error: {script} failed")
        sys.exit(1)


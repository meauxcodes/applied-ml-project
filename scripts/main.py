import subprocess
    
subprocess.run(["python", "garmin_pull.py"])
subprocess.run(["python", "garmin_clean.py"])
subprocess.run(["python", "visualizations.py"])
subprocess.run(["python", "cohort_stacking.py"])
subprocess.run(["python", "cohort_cleaning.py"])

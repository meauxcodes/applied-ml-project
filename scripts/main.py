import subprocess
    
subprocess.run(["python", "garmin_pull.py"])
subprocess.run(["python", "garmin_clean.py"])
subprocess.run(["python", "visualizations.py"])
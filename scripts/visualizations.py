import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns   

clean_data = pd.read_csv("../data/clean/cleaned_garmin_data.csv")

### Visualization #1 ###
### Sleep Stage breakdown over time ###
deep = clean_data["deep sleep seconds"]
light = clean_data["light sleep seconds"]
rem = clean_data["rem sleep seconds"]
awake = clean_data["awake sleep seconds"]

fig, ax = plt.subplots()
ax.bar(clean_data["date"], rem / 3600, label = "REM Sleep", color = "#8A97B8")
ax.bar(clean_data["date"], deep / 3600, label = "Deep Sleep", color = "#9C4438", bottom = rem / 3600)
ax.bar(clean_data["date"], light / 3600, label = "Light Sleep", color = "#A6841F", bottom = (rem + deep) / 3600)
ax.bar(clean_data["date"], awake / 3600, label = "Awake", color = "#1B2340", bottom = (rem + deep + light) / 3600)
ax.set_title("Sleep Stage Duration Over Time")
ax.set_ylabel("Duration (hours)")
ax.set_xlabel("Date")
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

plt.xticks(rotation = 90)
plt.tight_layout()
plt.savefig("../images/dataprep/sleep_stage_over_time_bar.png")
plt.close()

### Visualization #2 ###
### Overnight HRV vs Average Daily Stress ###

fig, ax = plt.subplots()
ax.scatter(clean_data["hrv last night avg"], clean_data["avg stress"], color="#9C4438")
ax.set_title("Overnight HRV vs. Next-Day Average Stress")
ax.set_xlabel("Overnight HRV (ms)")
ax.set_ylabel("Next-Day Average Stress")

plt.tight_layout()
plt.savefig("../images/dataprep/hrv_vs_next_day_stress_scatter.png")
plt.close()


### Visualization #3 ###
### Total Calories vs HRV (Scatterplot) ###

fig, ax = plt.subplots()
ax.scatter(clean_data["total calories"], clean_data["hrv last night avg"], label="Total Calories Burned vs HRV", color="#9C4438")
ax.set_title("Total Calories Burned vs Overnight HRV (Avg)")
ax.set_ylabel("Overnight HRV (Avg)")
ax.set_xlabel("Total Calories Burned")

plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig("../images/dataprep/total_calories_vs_hrv_scatter.png")
plt.close()

### Visualization #4 ###
### Total Steps vs Next Night Sleep Score (Scatterplot) ###

fig, ax = plt.subplots()
ax.scatter(clean_data["total steps"], clean_data["overall sleep score"].shift(-1), label="Total Steps vs Next Night Sleep Score", color="#8A97B8")
ax.set_title("Total Steps vs Next Night Sleep Score")
ax.set_ylabel("Next Night Sleep Score")
ax.set_xlabel("Total Steps")

plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig("../images/dataprep/total_steps_vs_next_night_sleep_score_scatter.png")
plt.close()

### Visualization #5 ###
### Body Battery Charged vs Drained ###

clean_data.plot(x = "date", y = ["body battery charged", "body battery drained"], kind = "bar", color = ["#8A97B8", "#9C4438"])
plt.title("Body Battery Charged vs Drained")
plt.ylabel("Body Battery Score")
plt.xlabel("Date")
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig("../images/dataprep/body_battery_charged_vs_drained_bar.png")
plt.close()

### Visualization #6 ###
### Body Battery Drained vs. Overall Sleep Score ###

fig, ax = plt.subplots()
ax.scatter(clean_data["body battery drained"], clean_data["overall sleep score"].shift(-1), label="Body Battery Drained vs Next Night Sleep Score", color="#1B2340")
ax.set_title("Body Battery Drained vs Next Night Sleep Score")
ax.set_ylabel("Next Night Sleep Score")
ax.set_xlabel("Body Battery Drained")

plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig("../images/dataprep/body_battery_drained_vs_next_night_sleep_score_scatter.png")
plt.close()

### Visualization #7 ###
### Average Respiration Rate (Sleep) over Time ###

fig, ax = plt.subplots()
ax.plot(clean_data["date"],clean_data["avg respiration (sleep)"],label="Avg Respiration Rate (Sleep)",marker = "o", color="#A6841F")
ax.set_title("Average Respiration Rate (Sleep) over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Average Respiration Rate (Sleep)")

plt.xticks(rotation = 90)
plt.tight_layout()
plt.savefig("../images/dataprep/average_respiration_rate_sleep_over_time.png")
plt.close()


### Visualization #8 ###
### Average Respiration Rate (Sleep) vs Overall Sleep Score ###

fig, ax = plt.subplots()
ax.scatter(clean_data["overall sleep score"],clean_data["avg respiration (sleep)"],label="Avg Respiration Rate (Sleep)",marker = "o", color="#A6841F")
ax.set_title("Average Respiration Rate (Sleep) vs Sleep Score")
ax.set_xlabel("Overall Sleep Score")
ax.set_ylabel("Average Respiration Rate (Sleep)")

plt.xticks(rotation = 90)
plt.tight_layout()
plt.savefig("../images/dataprep/average_respiration_rate_sleep_vs_sleep_score.png")
plt.close()


### Visualization #9 ###
### Average Sleep Stress Over Time ###

fig, ax = plt.subplots()
ax.plot(clean_data["date"],clean_data["avg sleep stress"],label="Avg Sleep Stress",marker = "o", color="#9C4438")
ax.set_title("Average Sleep Stress Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Average Sleep Stress")

plt.xticks(rotation = 90)
plt.tight_layout()
plt.savefig("../images/dataprep/average_sleep_stress_over_time.png")
plt.close()


### Visualization #10 ###
### Average Resting Heart Rate Over Time ###

fig, ax = plt.subplots()
ax.plot(clean_data["date"],clean_data["resting heart rate (overnight)"],label="Avg Resting Heart Rate",marker = "o", color="#9C4438")
ax.set_title("Average Resting Heart Rate Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Average Resting Heart Rate")

plt.xticks(rotation = 90)
plt.tight_layout()
plt.savefig("../images/dataprep/average_resting_heart_rate_over_time.png")
plt.close()


### Visualization #11 ###
### Sleep Score Distribution ###

fig, ax = plt.subplots()
ax.hist(clean_data["overall sleep score"], bins=5, color="#A6841F", alpha=0.7)
ax.set_title("Sleep Score Distribution")
ax.set_xlabel("Sleep Score")

plt.tight_layout()
plt.savefig("../images/dataprep/sleep_score_distribution.png")
plt.close()


### Visualization #12 ###
### Recovery Metric Boxplots ###
plot_data = [
    clean_data["overall sleep score"],
    clean_data["avg sleep stress"],
    clean_data["deep sleep percent"],
    clean_data["rem sleep percent"]
]
fig, ax = plt.subplots()
ax.boxplot(plot_data, patch_artist=True, boxprops=dict(facecolor="#8A97B8", alpha=0.7))
ax.set_title("Recovery Metrics Boxplots")
ax.set_ylabel("Score")
ax.set_xlabel("Metric")
ax.set_xticklabels(["Overall Sleep Score", "Avg Sleep Stress", "Deep Sleep %", "REM Sleep %"])


plt.tight_layout()
plt.savefig("../images/dataprep/recovery_metrics_boxplots.png")
plt.close()


### Visualization #13 ###
### Correlation Heat Map ###

# From the eda_exploration notebook:

corr_columns = [
   "avg overnight HRV",
   "overall sleep score",
   "avg sleep stress",
   "resting heart rate",
   "body battery drained",
   "avg respiration (sleep)",
   "body battery charged",
   "deep sleep seconds",
   "rem sleep seconds",
   "sleep total seconds",
   "vigorous intensity minutes",
   "min heart rate",
   "awake count"
]
correlation_data = clean_data[corr_columns].copy()
correlation_data["previous day body battery drained"] = clean_data["body battery drained"].shift(1)

# Plotting the heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_data.corr(), annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar_kws={"shrink": .8})
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("../images/dataprep/correlation_heatmap.png")
plt.close()


### Visualization #14 ###
### Intensity Minutes by Day###

fig, ax = plt.subplots()
ax.bar(clean_data["date"],clean_data["moderate intensity minutes"],label="Moderate Intensity Minutes",color="#8A97B8")
ax.bar(clean_data["date"],clean_data["vigorous intensity minutes"],label="Vigorous Intensity Minutes",color="#9C4438")
ax.set_title("Intensity Minutes by Day")
ax.set_xlabel("Date")
ax.set_ylabel("Intensity Minutes")
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

plt.xticks(rotation = 90)
plt.tight_layout()
plt.savefig("../images/dataprep/intensity_minutes_by_day.png")
plt.close()

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

##AI Tools were utilized to help verify plotting script and day-order script (shift)

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
plt.xticks()
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
site_cmap = LinearSegmentedColormap.from_list("site_diverging", ["#8A97B8", "#EDEFF5", "#C9645A"])
# Plotting the heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_data.corr(), annot=True, fmt=".2f", cmap=site_cmap, square=True, cbar_kws={"shrink": .8})
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


### Visualization #15 ###
### Redrawn NVSD Graph ###

sleep_apnea = np.array([1.0, 0.40, 3.2, 1.3, 6.6, 2.6])
insomnia = np.array([0.75, 0.25, 2.3, 0.5, 5.1, 1.1])
other = np.array([0.85, 0.15, 1.2, 0.2, 2.3, 0.65])
small_types = np.array([0.6, 0.05, 1.5, 0.35, 2.05, 0.35])
x = [0, 1, 2.5, 3.5, 5, 6]
total_percentages = [3.2, 0.9, 8.2, 2.4, 16.1, 4.7]

fig, ax = plt.subplots()
ax.bar(x, sleep_apnea, label = "Sleep Apnea", color = "#9C4438")
ax.bar(x, insomnia, label = "Insomnia", color = "#8A97B8", bottom = sleep_apnea)
ax.bar(x, other, label = "Other Sleep Disorders", color = "#A6841F", bottom = sleep_apnea + insomnia)
bars = ax.bar(x, small_types, label = "Hypersomnia, Movement, Parasomnia", color = "#1B2340", bottom = sleep_apnea + insomnia + other)
ax.bar_label(bars, labels=[f"~{v:.1f}%" for v in total_percentages], fontsize=10, padding=2)
ax.set_xticks(x)
ax.set_xticklabels(["PTSD","No PTSD","PTSD","No PTSD","PTSD","No PTSD"])
ax.text(0.5, -0.13, "FY 2000", transform=ax.get_xaxis_transform(), ha="center")
ax.text(3.0, -0.13, "FY 2005", transform=ax.get_xaxis_transform(), ha="center")
ax.text(5.5, -0.13, "FY 2010", transform=ax.get_xaxis_transform(), ha="center")
ax.set_title("Diagnosed Sleep Disorders Among Veterans in VA Care, by PTSD Status", fontsize = 11)
ax.set_ylabel("% of group with a diagnosed sleep disorder")
ax.legend(loc="upper left")
plt.tight_layout()
plt.savefig("../images/intro/ptsd_sleep_disorders.png", bbox_inches="tight")
plt.close()


##########################################################
### COHORT (98 PARTICIPANTS) VISUALIZATIONS ###
##########################################################

##AI Tools were utilized to help verify plotting script and day-order script

cohort = pd.read_csv("../data/clean/cohort_cleaned.csv") #reading in the cohort data
cohort["calendarDate"] = pd.to_datetime(cohort["calendarDate"]) #the data has a weird timestamp so I'm converting that to an actual calendar date
cohort = cohort.sort_values(["participant_id", "calendarDate"]).reset_index(drop=True) #my rows are not in order so I'm sorting them by participant and then by date
cohort["total calories"] = cohort["bmrKilocalories"] +cohort["activeKilocalories"] #these three features didn't exist in the cohort data so I'm adding them to the dataset
cohort["deep sleep percent"] = cohort["deepSleepDurationInMs"] / cohort["durationInMs"] * 100
cohort["rem sleep percent"] = cohort["remSleepInMs"] / cohort["durationInMs"] * 100


next_date = cohort.groupby("participant_id")["calendarDate"].shift(-1) # Values for stress and other daily activity metrics have to be shifted one calendar day earlier so that they are accounted for before the sleep metrics
is_next_day = (next_date - cohort["calendarDate"]).dt.days == 1 #this is a check for making sure that the dates line up as stated above
cohort["next day calories"] = cohort.groupby("participant_id")["total calories"].shift(-1).where(is_next_day) # placing next day calorie levels where they belong in the order of days
cohort["next day stress"] = cohort.groupby("participant_id")["averageStressInStressLevel"].shift(-1).where(is_next_day) # placing next day stress levels where they belong in the order of days



### Cohort Visualization match with N-of-1 visualization #2 ###
### Overnight HRV vs Next-Day Average Stress ###

fig, ax = plt.subplots()
ax.scatter(cohort["lastNightAvg"], cohort["next day stress"], color="#9C4438", s=6, alpha=0.3)
ax.set_title("Overnight HRV vs. Next-Day Average Stress (98 Participants)")
ax.set_xlabel("Overnight HRV (ms)")
ax.set_ylabel("Next-Day Average Stress")

plt.tight_layout()
plt.savefig("../images/dataprep/cohort_hrv_vs_next_day_stress_scatter.png")
plt.close()


### Cohort Visualization match with N-of-1 visualization #3 ###
### Total Calories vs HRV (Scatterplot) ###

fig, ax = plt.subplots()
ax.scatter(cohort["next day calories"], cohort["lastNightAvg"], color="#9C4438", s=6, alpha=0.3)
ax.set_title("Total Calories Burned vs Overnight HRV (98 Participants)")
ax.set_ylabel("Overnight HRV (Avg)")
ax.set_xlabel("Total Calories Burned")

plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig("../images/dataprep/cohort_total_calories_vs_hrv_scatter.png")
plt.close()


### Cohort Visualization match with N-of-1 visualization #4 ###
### Total Steps vs Next Night Sleep Score (Scatterplot) ###

fig, ax = plt.subplots()
ax.scatter(cohort["steps"], cohort["overallSleepScore"], color="#8A97B8", s=6, alpha=0.3)
ax.set_title("Total Steps vs Next Night Sleep Score (98 Participants)")
ax.set_ylabel("Next Night Sleep Score")
ax.set_xlabel("Total Steps")

plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig("../images/dataprep/cohort_total_steps_vs_next_night_sleep_score_scatter.png")
plt.close()


### Cohort Visualization match with N-of-1 visualization #8 ###
### Average Respiration Rate (Sleep) vs Overall Sleep Score ###

fig, ax = plt.subplots()
ax.scatter(cohort["overallSleepScore"], cohort["breathsPerMinute_mean"], color="#A6841F", s=6, alpha=0.3)
ax.set_title("Average Respiration Rate (Sleep) vs Sleep Score (98 Participants)")
ax.set_xlabel("Overall Sleep Score")
ax.set_ylabel("Average Respiration Rate (Sleep)")

plt.tight_layout()
plt.savefig("../images/dataprep/cohort_average_respiration_rate_sleep_vs_sleep_score.png")
plt.close()


### Cohort Visualization match with N-of-1 visualization #11 ###
### Sleep Score Distribution ###

fig, ax = plt.subplots()
ax.hist(cohort["overallSleepScore"], bins=20, color="#A6841F", alpha=0.7)
ax.set_title("Sleep Score Distribution (98 Participants)")
ax.set_xlabel("Sleep Score")
ax.set_ylabel("Number of Nights")

plt.tight_layout()
plt.savefig("../images/dataprep/cohort_sleep_score_distribution.png")
plt.close()


### Cohort Visualization match with N-of-1 visualization #12 ###
### Recovery Metric Boxplots ###

plot_data = [
    cohort["overallSleepScore"],
    cohort["averageStressInStressLevel"],
    cohort["deep sleep percent"],
    cohort["rem sleep percent"]
]
fig, ax = plt.subplots()
ax.boxplot(plot_data, patch_artist=True, boxprops=dict(facecolor="#8A97B8", alpha=0.7))
ax.set_title("Recovery Metrics Boxplots (98 Participants)")
ax.set_ylabel("Score")
ax.set_xlabel("Metric")
ax.set_xticklabels(["Overall Sleep Score", "Avg Daily Stress", "Deep Sleep %", "REM Sleep %"])

plt.tight_layout()
plt.savefig("../images/dataprep/cohort_recovery_metrics_boxplots.png")
plt.close()


### Cohort Visualization match with N-of-1 visualization #13 ###
### Correlation Heat Map ###


cohort_corr_columns = [
    "lastNightAvg",
    "overallSleepScore",
    "averageStressInStressLevel",
    "restingHeartRateInBeatsPerMinute",
    "minHeartRateInBeatsPerMinute",
    "breathsPerMinute_mean",
    "deepSleepDurationInMs",
    "remSleepInMs",
    "durationInMs",
    "vigorousIntensityDurationInMs",
    "steps",
    "awakeDurationInMs"
]

site_cmap = LinearSegmentedColormap.from_list("site_diverging", ["#8A97B8", "#EDEFF5", "#C9645A"])
plt.figure(figsize=(12, 10))
sns.heatmap(cohort[cohort_corr_columns].corr(), annot=True, fmt=".2f", cmap=site_cmap, square=True, cbar_kws={"shrink": .8})
plt.title("Correlation Heatmap (98 Participants)")
plt.tight_layout()
plt.savefig("../images/dataprep/cohort_correlation_heatmap.png")
plt.close()

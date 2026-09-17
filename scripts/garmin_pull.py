from dotenv import load_dotenv
load_dotenv()

import os
import time
from pathlib import Path
import pandas as pd

email = os.environ.get("GARMIN_EMAIL")
password = os.environ.get("GARMIN_PASSWORD")

# the below code was provided by: github.com/cyberjunky/python-garminconnect
from datetime import date, timedelta
from garminconnect import Garmin

# First run: logs in and saves tokens to ~/.garminconnect
# Subsequent runs: loads saved tokens and auto-refreshes
print("Creating session....")
client = Garmin(
    email,
    password
)
client.login("~/.garminconnect")
# the above code was provided by: github.com/cyberjunky/python-garminconnect
print("...session created")


### This below function takes the current date, and builds a list of all dates 
### from September 4th, 2026 (when I started wearing my Garmin), until the 
### current date. 

print("Script stopwatch started...")
time_start = time.time()

print("Calculating dates since 4 SEP 2026")
def calculate_dates():
    start_date = date(2026,9,4)
    day_total = date.today()-start_date
    dates = []
    for i in range(0,day_total.days + 1):
        dates.append((start_date+timedelta(days = i)).isoformat())
        
    return dates

dates = calculate_dates()

print("Pulling new Garmin data...")
if Path("../data/raw/sam_garmin_data.csv").exists():
    # the file exists so only pull up to today's date and repull the two previous days's data to grab any potential missed data.

    recent_days = [(date.today() - timedelta(days=i)).isoformat() for i in range(0, 2)]
    existing_data = pd.read_csv("../data/raw/sam_garmin_data.csv")
    existing_dates = existing_data["date"]
    new_data = []
    for day in dates:
        if day not in existing_dates.values or day in recent_days:
            try: #this will identify if any days don't get pulled for whatever reason; namely rate limiting
                heart_rate_data = client.get_heart_rates(day)
                time.sleep(2)
                stress_data = client.get_stress_data(day)
                time.sleep(2)
                body_battery = client.get_body_battery(day, day)
                time.sleep(2)
                sleep = client.get_sleep_data(day)
                time.sleep(2)
                steps = client.get_steps_data(day)
                time.sleep(2)
                resting_heart_rate = client.get_rhr_daily(day, day)
                time.sleep(2)
                calories = client.get_calories_daily(day, day)
                time.sleep(2)
                respiration = client.get_respiration_data(day)
                time.sleep(2)
                spo2 = client.get_spo2_data(day)
                time.sleep(2)
                hrv = client.get_hrv_data(day)
                time.sleep(2)
                intensity_minutes = client.get_intensity_minutes_data(day)
                time.sleep(2)

                day_data = {
                    "date": day,
                    "body battery charged": body_battery[0]["charged"],
                    "body battery drained": body_battery[0]["drained"],             
                    "sleep total seconds": sleep["dailySleepDTO"]["sleepTimeSeconds"],
                    "deep sleep seconds": sleep["dailySleepDTO"]["deepSleepSeconds"],
                    "light sleep seconds": sleep["dailySleepDTO"]["lightSleepSeconds"],
                    "rem sleep seconds": sleep["dailySleepDTO"]["remSleepSeconds"],
                    "awake sleep seconds": sleep["dailySleepDTO"]["awakeSleepSeconds"],
                    "avg respiration (sleep)": sleep["dailySleepDTO"]["averageRespirationValue"],
                    "min respiration (sleep)": sleep["dailySleepDTO"]["lowestRespirationValue"],
                    "max respiration (sleep)": sleep["dailySleepDTO"]["highestRespirationValue"],
                    "awake count": sleep["dailySleepDTO"]["awakeCount"],
                    "avg sleep stress": sleep["dailySleepDTO"]["avgSleepStress"],
                    "avg heart rate (sleep)": sleep["dailySleepDTO"]["avgHeartRate"],
                    "overall sleep score": sleep["dailySleepDTO"]["sleepScores"]["overall"]["value"],
                    "deep sleep percent": sleep["dailySleepDTO"]["sleepScores"]["deepPercentage"]["value"],
                    "rem sleep percent": sleep["dailySleepDTO"]["sleepScores"]["remPercentage"]["value"],
                    "light sleep percent": sleep["dailySleepDTO"]["sleepScores"]["lightPercentage"]["value"],
                    "resting heart rate (overnight)": sleep["restingHeartRate"],
                    "body battery change (overnight)": sleep["bodyBatteryChange"],
                    "avg overnight HRV": sleep["avgOvernightHrv"],
                    "total steps": sum(entry["steps"] for entry in steps),
                    "resting heart rate": resting_heart_rate[0]["value"],
                    "min heart rate": heart_rate_data["minHeartRate"],
                    "max heart rate": heart_rate_data["maxHeartRate"],
                    "7 day heart rate average": heart_rate_data["lastSevenDaysAvgRestingHeartRate"],
                    "max stress": stress_data["maxStressLevel"],
                    "avg stress": stress_data["avgStressLevel"],
                    "active calories": calories[0]["active"],
                    "resting calories": calories[0]["resting"],
                    "total calories": calories[0]["total"],
                    "lowest respiration (all day)": respiration["lowestRespirationValue"],
                    "highest respiration (all day)": respiration["highestRespirationValue"],
                    "avg waking respiration": respiration["avgWakingRespirationValue"],
                    "avg SpO2": spo2["averageSpO2"],
                    "lowest SpO2": spo2["lowestSpO2"],
                    "7 day avg SpO2": spo2["lastSevenDaysAvgSpO2"],
                    "avg sleep SpO2": spo2["avgSleepSpO2"],
                    "hrv weekly avg": hrv["hrvSummary"]["weeklyAvg"],
                    "hrv last night avg": hrv["hrvSummary"]["lastNightAvg"],
                    "hrv last night 5min high": hrv["hrvSummary"]["lastNight5MinHigh"],
                    "moderate intensity minutes": intensity_minutes["moderateMinutes"],
                    "vigorous intensity minutes": intensity_minutes["vigorousMinutes"],
                    "weekly total intensity minutes": intensity_minutes["weeklyTotal"],
                }
                new_data.append(day_data)

            except Exception as e:
                print(f"Skipped {day}: {e}")

    new_dataframe = pd.DataFrame(new_data)    
    sam_garmin_data = pd.concat([existing_data, new_dataframe])
    sam_garmin_data = sam_garmin_data.drop_duplicates(subset="date", keep="last")
    sam_garmin_data.to_csv("../data/raw/sam_garmin_data.csv",index = False)
    print("...CSV written")


else:
    # no file so go ahead and pull everything
    result = []
    for day in dates:
        try:
            heart_rate_data = client.get_heart_rates(day)
            time.sleep(2)
            stress_data = client.get_stress_data(day)
            time.sleep(2)
            body_battery = client.get_body_battery(day, day)
            time.sleep(2)
            sleep = client.get_sleep_data(day)
            time.sleep(2)
            steps = client.get_steps_data(day)
            time.sleep(2)
            resting_heart_rate = client.get_rhr_daily(day, day)
            time.sleep(2)
            calories = client.get_calories_daily(day, day)
            time.sleep(2)
            respiration = client.get_respiration_data(day)
            time.sleep(2)
            spo2 = client.get_spo2_data(day)
            time.sleep(2)
            hrv = client.get_hrv_data(day)
            time.sleep(2)
            intensity_minutes = client.get_intensity_minutes_data(day)
            time.sleep(2)

            day_data = {
                "date": day,
                "body battery charged": body_battery[0]["charged"],
                "body battery drained": body_battery[0]["drained"],             
                "sleep total seconds": sleep["dailySleepDTO"]["sleepTimeSeconds"],
                "deep sleep seconds": sleep["dailySleepDTO"]["deepSleepSeconds"],
                "light sleep seconds": sleep["dailySleepDTO"]["lightSleepSeconds"],
                "rem sleep seconds": sleep["dailySleepDTO"]["remSleepSeconds"],
                "awake sleep seconds": sleep["dailySleepDTO"]["awakeSleepSeconds"],
                "avg respiration (sleep)": sleep["dailySleepDTO"]["averageRespirationValue"],
                "min respiration (sleep)": sleep["dailySleepDTO"]["lowestRespirationValue"],
                "max respiration (sleep)": sleep["dailySleepDTO"]["highestRespirationValue"],
                "awake count": sleep["dailySleepDTO"]["awakeCount"],
                "avg sleep stress": sleep["dailySleepDTO"]["avgSleepStress"],
                "avg heart rate (sleep)": sleep["dailySleepDTO"]["avgHeartRate"],
                "overall sleep score": sleep["dailySleepDTO"]["sleepScores"]["overall"]["value"],
                "deep sleep percent": sleep["dailySleepDTO"]["sleepScores"]["deepPercentage"]["value"],
                "rem sleep percent": sleep["dailySleepDTO"]["sleepScores"]["remPercentage"]["value"],
                "light sleep percent": sleep["dailySleepDTO"]["sleepScores"]["lightPercentage"]["value"],
                "resting heart rate (overnight)": sleep["restingHeartRate"],
                "body battery change (overnight)": sleep["bodyBatteryChange"],
                "avg overnight HRV": sleep["avgOvernightHrv"],
                "total steps": sum(entry["steps"] for entry in steps),
                "resting heart rate": resting_heart_rate[0]["value"],
                "min heart rate": heart_rate_data["minHeartRate"],
                "max heart rate": heart_rate_data["maxHeartRate"],
                "7 day heart rate average": heart_rate_data["lastSevenDaysAvgRestingHeartRate"],
                "max stress": stress_data["maxStressLevel"],
                "avg stress": stress_data["avgStressLevel"],
                "active calories": calories[0]["active"],
                "resting calories": calories[0]["resting"],
                "total calories": calories[0]["total"],
                "lowest respiration (all day)": respiration["lowestRespirationValue"],
                "highest respiration (all day)": respiration["highestRespirationValue"],
                "avg waking respiration": respiration["avgWakingRespirationValue"],
                "avg SpO2": spo2["averageSpO2"],
                "lowest SpO2": spo2["lowestSpO2"],
                "7 day avg SpO2": spo2["lastSevenDaysAvgSpO2"],
                "avg sleep SpO2": spo2["avgSleepSpO2"],
                "hrv weekly avg": hrv["hrvSummary"]["weeklyAvg"],
                "hrv last night avg": hrv["hrvSummary"]["lastNightAvg"],
                "hrv last night 5min high": hrv["hrvSummary"]["lastNight5MinHigh"],
                "moderate intensity minutes": intensity_minutes["moderateMinutes"],
                "vigorous intensity minutes": intensity_minutes["vigorousMinutes"],
                "weekly total intensity minutes": intensity_minutes["weeklyTotal"],
            }
            result.append(day_data)
        except Exception as e:
            print(f"Skipped {day}: {e}")

 
    print("...Garmin data pulled")
    print("Writing Garmin data to CSV...")     
    sam_garmin_data = pd.DataFrame(result)
    sam_garmin_data.to_csv("../data/raw/sam_garmin_data.csv",index = False)
    print("...CSV written")

time_end = time.time()
print("Script stopwatch ended...")
print(f"It took {time_end - time_start} seconds to complete this data pull.")
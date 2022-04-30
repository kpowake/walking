import pandas as pd

pd.set_option('display.max_rows', None)

apple1_df = pd.read_csv("applehealth/HKQuantityTypeIdentifierDistanceWalkingRunning_SimpleHealthExportCSV.csv", header=1)
apple1_df["日付"] = pd.to_datetime(apple1_df["startDate"]).dt.tz_convert("Asia/Tokyo").dt.date
apple1_df["距離"] = apple1_df["value"]
apple1_df = apple1_df[["日付", "距離"]]
apple1_df = apple1_df.groupby(["日付"]).sum().reset_index()
apple1_df["距離"] = apple1_df["距離"].multiply(1000).astype("int")
apple2_df = pd.read_csv("applehealth/HKQuantityTypeIdentifierStepCount_SimpleHealthExportCSV.csv", header=1)
apple2_df["日付"] = pd.to_datetime(apple2_df["startDate"]).dt.tz_convert("Asia/Tokyo").dt.date
apple2_df["歩数"] = apple2_df["value"]
apple2_df = apple2_df[["日付", "歩数"]]
apple2_df = apple2_df.groupby(["日付"]).sum().reset_index()
apple2_df["歩数"] = apple2_df["歩数"].astype("int")
apple_df = pd.merge(apple2_df, apple1_df, on="日付")

google_df = pd.read_csv("googlefit/日別のアクティビティ指標.csv")
google_df["日付"] = pd.to_datetime(google_df["日付"]).dt.date
google_df["距離"] = google_df["距離（m）"]
google_df = google_df[["日付", "歩数", "距離"]]
google_df["距離"] = google_df["距離"].fillna(0).astype("int")

stepsapp_ios_df = pd.read_csv("stepsapp/activity-export-HourlyStep.csv", sep=";")
stepsapp_ios_df["日付"] = pd.to_datetime(stepsapp_ios_df["date"]).dt.date
stepsapp_ios_df["歩数"] = stepsapp_ios_df["steps"]
stepsapp_ios_df["距離"] = stepsapp_ios_df["distance [m]"]
stepsapp_ios_df = stepsapp_ios_df[["日付", "歩数", "距離"]]
stepsapp_ios_df = stepsapp_ios_df.groupby(["日付"]).sum().reset_index()
stepsapp_ios_df["距離"] = stepsapp_ios_df["距離"].astype("int")

stepsapp_android_df = pd.read_csv("stepsapp1/activity-export-hourly.csv", sep=";", usecols=[0,1,2,3,4], skiprows=[1])
stepsapp_android_df["日付"] = pd.to_datetime(stepsapp_android_df["date"]).dt.date
stepsapp_android_df["歩数"] = stepsapp_android_df["steps"]
stepsapp_android_df["距離"] = stepsapp_android_df["distance [m]"]
stepsapp_android_df = stepsapp_android_df[["日付", "歩数", "距離"]]
stepsapp_android_df = stepsapp_android_df.groupby(["日付"]).sum().reset_index()
stepsapp_android_df["距離"] = stepsapp_android_df["距離"].astype("int")

df = pd.concat([apple_df, google_df, stepsapp_ios_df, stepsapp_android_df]).groupby(["日付"]).max().reset_index()

df.to_csv("walking.csv", index=False)

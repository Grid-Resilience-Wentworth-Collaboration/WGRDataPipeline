import datetime
from dotenv import load_dotenv
import os
import pandas as pd
import gridstatus
import glob
import json


class DataGaps:

    def __init__(self):
        pass

    def isComplete(self) -> bool:
        return True

    def getGaps(self) -> dict:
        return {}


class DataGatherer:

    def __init__(self):
        pass

    def gatherCAISO_LMPData(self, date: datetime) -> None:
        load_dotenv()
        # use https://docs.gridstatus.io/en/latest/lmp.html to gather data and save to folder
        # pointed to by LMP_DATA_PATH environment variable
        caiso = gridstatus.CAISO()
        gather_date = date.strftime("%Y-%m-%d")
        data = caiso.get_lmp(
            date=gather_date,
            market="DAY_AHEAD_HOURLY",
            locations="ALL",
        )
        data.to_csv(f'{os.getenv("LMP_DATA_PATH")}/{gather_date}.csv')


class DataAvailibility:

    def __init__(
        self,
        nodeID: str,
        forcastAt: datetime.datetime,
        toleranceMinutes: float,
        historyHours: int,
    ):
        load_dotenv()
        self.nodeID = nodeID
        self.forcastAt = forcastAt
        self.toleranceMinutes = toleranceMinutes
        self.historyHours = historyHours

        self.LMP_DATA_PATH = os.getenv("LMP_DATA_PATH")
        self.LMP_DATA_TIMEZONE = os.getenv("LMP_DATA_TIMEZONE")

    def getDataGaps(self) -> DataGaps:
        # Start by analyzing whether historical LMP data are available for given date range
        # For now we will assume that the datetime input is in UTC and we will convert it to given timezone for querying
        # existence of data files in the file system
        for i in range(0, self.historyHours):
            pass
        return None


class SeriesCreator:

    def __init__(
        self,
        nodeId: str,
        forcastAt: datetime.datetime,
        toleranceMinutes: float,
        historyHours: int,
    ):
        self.nodeId = nodeId
        self.forcastAt = forcastAt
        self.toleranceMinutes = toleranceMinutes
        self.historyHours = historyHours
        pass

    def getClosestForcast(self) -> dict:
        pattern = f'{os.getenv("SERIES_CREATOR_WEATHER_FORECAST_PATH")}/{self.nodeId}-{self.forcastAt.strftime("%Y-%m-%d")}*.json'
        file_list = glob.glob(pattern)
        return json.load(open(file_list[0]))

    def createTrainingSeriesV1(self) -> dict:

        series = dict()
        series["nodeId"] = self.nodeId
        series["forecastAt"] = self.forcastAt
        series["toleranceMinutes"] = self.toleranceMinutes
        series["historyHours"] = self.historyHours
        series["series"] = []
        series["weatherForecast"] = self.getClosestForcast()
        series["LMPForecast"] = []

        START = self.forcastAt
        END = self.forcastAt - datetime.timedelta(hours=self.historyHours)
        while START >= END:
            START_STR = START.strftime("%Y-%m-%d")
            print(f"Getting data for {START_STR}")
            if not os.path.exists(f'{os.getenv("LMP_DATA_PATH")}/{START_STR}.csv'):
                raise Exception(f"Data does not exists for {START_STR}")
            data = pd.read_csv(
                f'{os.getenv("LMP_DATA_PATH")}/{START_STR}.csv',
                parse_dates=[0, 1],
                date_format="mixed",
            )
            data = data[data["Location"] == self.nodeId]
            for i in range(0, len(data)):
                data_row = data.iloc[i]
                if data_row["Time"] >= START:
                    data_item = dict()
                    data_item["Time"] = data_row["Time"]
                    data_item["LMP"] = data_row["LMP"]
                    series["series"].append(data_item)
                START = START - datetime.timedelta(hours=1)
                if START < END:
                    break

        START = self.forcastAt
        END = self.forcastAt + datetime.timedelta(hours=168)  # 7 days
        while START <= END:
            START_STR = START.strftime("%Y-%m-%d")
            print(f"Getting data for {START_STR}")
            if not os.path.exists(f'{os.getenv("LMP_DATA_PATH")}/{START_STR}.csv'):
                raise Exception(f"Data does not exists for {START_STR}")
            data = pd.read_csv(
                f'{os.getenv("LMP_DATA_PATH")}/{START_STR}.csv',
                parse_dates=[0, 1],
                date_format="mixed",
            )
            data = data[data["Location"] == self.nodeId]
            for i in range(0, len(data)):
                data_row = data.iloc[i]
                if data_row["Time"] <= START:
                    data_item = dict()
                    data_item["Time"] = data_row["Time"]
                    data_item["LMP"] = data_row["LMP"]
                    series["LMPForecast"].append(data_item)
                START = START + datetime.timedelta(hours=1)
                if START > END:
                    break
        return series

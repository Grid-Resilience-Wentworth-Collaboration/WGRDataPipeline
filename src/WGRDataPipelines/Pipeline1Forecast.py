import datetime
from dotenv import load_dotenv
import os
import pandas as pd
import gridstatus
import glob
import json


class DataGaps:

    def __init__(self):
        self.gaps = {"LMP_GAPS": {}}

    def isComplete(self) -> bool:
        return len(self.gaps) == 0

    def getGaps(self) -> dict:
        return self.gaps


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


class DataAvailability:

    def __init__(
        self,
        nodeID: str,
        forecastAt: datetime.datetime,
        toleranceMinutes: float,
        historyHours: int,
    ):
        load_dotenv()
        self.nodeID = nodeID
        self.forcastAt = forecastAt
        self.toleranceMinutes = toleranceMinutes
        self.historyHours = historyHours
        self.hourlyIncrement = 1
        self.LMP_DATA_PATH = os.getenv("LMP_DATA_PATH")
        self.LMP_DATA_TIMEZONE = os.getenv("LMP_DATA_TIMEZONE")

    def is_dst(self, date):
        year = date.year
        # Find the second Sunday in March
        second_sunday_march = datetime.datetime(year, 3, 8) + datetime.timedelta(
            days=(6 - datetime.datetime(year, 3, 8).weekday())
        )
        # Find the first Sunday in November
        first_sunday_november = datetime.datetime(year, 11, 1) + datetime.timedelta(
            days=(6 - datetime.datetime(year, 11, 1).weekday())
        )

        return second_sunday_march <= date < first_sunday_november

    def getDataGaps(self) -> DataGaps:
        # Start by analyzing whether historical LMP data are available for given date range
        # For now we will assume that the datetime input is in UTC and we will convert it to given timezone for querying
        # existence of data files in the file system
        END = self.forcastAt
        START = END - datetime.timedelta(hours=self.historyHours)
        data_gaps = DataGaps()
        while START <= END:
            START_STR = START.strftime("%Y-%m-%d")
            file_path = f'{os.getenv("LMP_DATA_PATH")}/{START_STR}.csv'
            current_time = START
            is_dst = self.is_dst(START)
            with open(file=file_path, mode="r") as file:
                rows = pd.read_csv(file)
                rows = rows[rows["Location"] == self.nodeId]
                # TODO: Check data availability for given START within tolerance
                lower_bound = current_time - datetime.timedelta(
                    minutes=self.toleranceMinutes
                )
                upper_bound = current_time + datetime.timedelta(
                    minutes=self.toleranceMinutes
                )
                rows_within_tol = rows[
                    (rows["Time"] >= lower_bound) and (rows["Time"] <= upper_bound)
                ]
                if len(rows_within_tol) == 0:
                    data_gaps.gaps["LMP_GAPS"][self.nodeID] = current_time
                current_time += datetime.timedelta(hours=self.hourlyIncrement)

            START = START + datetime.timedelta(days=1)

        return data_gaps.getGaps()


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
        return series

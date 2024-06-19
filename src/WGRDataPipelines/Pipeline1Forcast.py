import datetime
from dotenv import load_dotenv
import os
import pandas as pd
from dateutil import parser
import gridstatus


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

    def __init__(self):
        pass

    def createSeriesV1(
        self,
        nodeID: str,
        forcastAt: datetime.datetime,
        toleranceMinutes: float,
        historyHours: int,
    ) -> None:
        self.nodeID = nodeID
        self.forcastAt = forcastAt
        self.toleranceMinutes = toleranceMinutes
        self.historyHours = historyHours

        series = dict()
        series["nodeID"] = nodeID
        series["forcastAt"] = forcastAt
        series["toleranceMinutes"] = toleranceMinutes
        series["historyHours"] = historyHours
        series["series"] = dict()

        START = forcastAt
        END = forcastAt - datetime.timedelta(hours=historyHours)
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
            data = data[data["Location"] == nodeID]
            for i in range(0, len(data)):
                data_row = data.iloc[i]
                if data_row["Time"] >= START:
                    series["series"][data_row["Time"]] = data_row["LMP"]
                START = START - datetime.timedelta(hours=1)
                if START < END:
                    break
        return series

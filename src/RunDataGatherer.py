from WGRDataPipelines.Pipeline1Forcast import DataGatherer
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

gatherer = DataGatherer()
START = datetime.datetime.strptime(os.getenv("LMP_DATA_GATHER_DATE_START"), "%Y-%m-%d")
END = datetime.datetime.strptime(os.getenv("LMP_DATA_GATHER_DATE_END"), "%Y-%m-%d")
while START <= END:
    START_STR = START.strftime("%Y-%m-%d")
    print(f"Getting data for {START_STR}")
    if os.path.exists(f'{os.getenv("LMP_DATA_PATH")}/{START_STR}.csv'):
        print(f"Data already exists for {START_STR}")
        START = START + datetime.timedelta(days=1)
        continue
    gatherer.gatherCAISO_LMPData(START)
    START = START + datetime.timedelta(days=1)

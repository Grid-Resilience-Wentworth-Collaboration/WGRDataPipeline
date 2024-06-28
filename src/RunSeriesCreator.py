from WGRDataPipelines.Pipeline1Forcast import SeriesCreator
from dateutil import parser
from dotenv import load_dotenv
import os
import json

load_dotenv()

NodeId = os.getenv("SERIES_CREATOR_NODE_ID")
START = parser.parse(os.getenv("SERIES_CREATOR_START_DATETIME"))
HOURS = int(os.getenv("SERIES_CREATOR_HISTORY_HOURS"))
TOL = int(os.getenv("SERIES_CREATOR_TOLERANCE_MINUTES"))
creator = SeriesCreator(NodeId, START, TOL, HOURS)
series = creator.createTrainingSeriesV1()
OUTPUT_PATH = os.getenv("SERIES_CREATOR_OUTPUT_PATH")

with open(f"{OUTPUT_PATH}/{NodeId}-{START}-{HOURS}.json", "w") as f:
    json.dump(series, f, indent=4, sort_keys=True, default=str)

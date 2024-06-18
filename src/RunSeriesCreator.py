from WGRDataPipelines.Pipeline1Forcast import DataGatherer
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

creator = DataGatherer()
NodeId = os.getenv("SERIES_CREATOR_NODE_ID")
START = datetime.datetime.strptime(
    os.getenv("SERIES_CREATOR_START_DATETIME"), "%Y-%m-%d %H:%M:%S"
)
HOURS = os.getenv("SERIES_CREATOR_HOURS")
TOL = os.getenv("SERIES_CREATOR_TOLERANCE")
creator.createSeriesV1(NodeId, START, TOL, HOURS)

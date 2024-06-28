from WGRDataPipelines.Pipeline1Forecast import DataAvailability
from dateutil import parser
from dotenv import load_dotenv
import os

load_dotenv()
NodeId = os.getenv("SERIES_CREATOR_NODE_ID")
START = parser.parse(os.getenv("SERIES_CREATOR_START_DATETIME"))
HOURS = int(os.getenv("SERIES_CREATOR_HISTORY_HOURS"))
TOL = int(os.getenv("SERIES_CREATOR_TOLERANCE_MINUTES"))

dataGapsChecker = DataAvailability(NodeId, START, TOL, HOURS)
print(dataGapsChecker.getDataGaps())

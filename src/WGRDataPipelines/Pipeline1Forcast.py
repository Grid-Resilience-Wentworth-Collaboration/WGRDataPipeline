from datetime import datetime


class DataGaps:

    def __init__(self):
        pass

    def isComplete(self) -> bool:
        return True

    def getGaps(self) -> dict:
        return []


class DataAvailibility:

    def __init__(
        self, nodeID: str, forcastAt: datetime, toleranceHours: int, historyDays: int
    ):
        self.nodeID = nodeID
        self.forcastAt = forcastAt
        self.toleranceHours = toleranceHours
        self.historyDays = historyDays

    def getDataGaps(self) -> DataGaps:

        return True

from datetime import datetime
import numpy as np


class DateCalculator:
    """
    Class to figure out the date
    """
    def __init__(self):
        self.now = datetime.now()

    def get_date(self) -> str:
        if self.now.hour < 5:  # before 5am
            return self._get_yesterday()
        date = self.now.date().strftime("%d/%m")
        date = date.replace("0", "")
        return date

    def _get_yesterday(self) -> str:
        yesterday = np.subtract(
            np.datetime64(self.now.date()),
            np.timedelta64(1, "D"),
            casting="unsafe"
        )
        month = str(yesterday).split("-")[1].replace("0", "")
        day = str(yesterday).split("-")[2].replace("0", "")
        correct_date = day + "/" + month
        return correct_date
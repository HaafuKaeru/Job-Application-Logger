from datetime import datetime


class DateCalculator:
    """
    Class to figure out the date
    """

    def __init__(self):
        self.now = datetime.now()

    def get_date(self) -> str:
        # TODO: use yesterday date when current time is between 00:00 and 03:00; yes I am a night owl.
        date = self.now.date().strftime("%d/%m")
        date = date.replace("0", "")
        return date

    def _get_yesterday(self):
        pass
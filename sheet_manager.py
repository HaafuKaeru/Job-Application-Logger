import requests
import os
from dotenv import load_dotenv


load_dotenv(".env")

class SheetManager:
    """
    Class to manage the Google sheet (Sheety API)
    """
    def __init__(self):
        self.bearer_token = os.getenv("SHEETY_JOB_APPLICATIONS_API_BEARER_TOKEN")
        self.url = os.getenv("SHEETY_JOB_APPLICATIONS_API_URL")

    def _api_header(self):
        auth_header = {
            "Authorization": f"Bearer {self.bearer_token}",
        }
        return auth_header

    def add_row(self, company_name, location, position_name, date, link, site):
        post_params = {
            "companiesList": {
                "company": company_name,
                "role": position_name,
                "link": link,
                "location": location,
                "date": date,
                "site": site,
                "cvStage": "",  # updated manually
                "interviewStage": "",  # updated manually
            }
        }
        rsp = requests.post(
            url=self.url,
            json=post_params,
            headers=self._api_header(),
        )
        rsp.raise_for_status()
        return rsp.json()
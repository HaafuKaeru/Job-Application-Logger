import requests
from bs4 import BeautifulSoup


class PageScraper:

    def __init__(self, url):
        self.url = url
        self.soup = None
        self._make_soup()

    def _make_soup(self):
        rsp = requests.get(self.url)
        rsp.raise_for_status()
        self.soup = BeautifulSoup(rsp.text, "html.parser")


class LinkedinScraper(PageScraper):
    """
    html scraper for webpage of the form
        https://www.linkedin.com/jobs/view/job_listing_number/
    """

    def __init__(self, url):
        super().__init__(url)
        self.site = "Linkedin"

    def get_company_name(self) -> str:
        # first h4 contains company name
        h4_tag = self.soup.find(name="h4")
        spans = h4_tag.select("span")
        company_name = spans[0].text.strip()
        return company_name

    def get_location(self) -> str:
        # first h4 contains office location
        h4_tag = self.soup.find(name="h4")
        spans = h4_tag.select("span")
        location = spans[1].text.strip()
        location = location.split(",")[0]  # get only first city name
        return location

    def get_position_name(self) -> str:
        # first h1 contains position name
        h1_tag = self.soup.find(name="h1")
        position_name = h1_tag.text.strip()
        return position_name


class IndeedScraper(PageScraper):

    def __init__(self, url):
        super().__init__(url)
        self.site = "Indeed"
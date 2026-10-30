from bs4 import BeautifulSoup
import requests
import os
import dotenv


dotenv.load_dotenv(".env")
USER_AGENT = os.getenv("user_agent")


class PageScraper:
    """
    Template class for other web scraping classes
    Also initialises the SOUP
    """
    def __init__(self, url):
        self.url = url
        self.user_agent = USER_AGENT
        self.soup = None
        self._make_soup()

    def _make_soup(self):
        headers = {
            'User-Agent': self.user_agent,
        }
        rsp = requests.get(self.url, headers=headers)
        rsp.raise_for_status()
        self.soup = BeautifulSoup(rsp.text, "html.parser")

    def get_position_name(self):
        # first h1 always (so far) contains position name
        h1_tag = self.soup.find(name="h1")
        position_name = h1_tag.text.strip()
        return position_name

    def get_company_name(self):
        pass

    def get_location(self):
        pass


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
        if location == "United Kingdom":
            return "Remote"
        return location


class IndeedScraper(PageScraper):
    """
    html scraper for pages of the form
        https://uk.indeed.com/viewjob?jk=job_listing_id&hl=en

    TODO: selenium might work?

    Failed attempts:
    https://learnwebscraping.substack.com/p/how-i-scraped-indeed-website
    https://daijro.gitbook.io/hrequests
    https://stackoverflow.com/questions/64409393/how-to-get-past-javascript-is-disabled-in-your-browser-error-when-web-scraping-w
    """

    def __init__(self, url):
        super().__init__(url)
        self.site = "Indeed"

    def get_position_name(self):
        # first h1 contains position name
        h1_tag = self.soup.find(name="h1")
        position_name = h1_tag.text.strip()
        return position_name

    def get_company_name(self):
        pass

    def get_location(self):
        pass


class TotalJobsScraper(PageScraper):
    """
    html scraper for pages of the form
        https://www.totaljobs.com/job/...
    """
    def __init__(self, url):
        super().__init__(url)
        self.site = "totaljobs"
        self.ul_element = self._get_unordered_list_element()

    def _get_unordered_list_element(self):
        # all useful info sits in the header, which is the first <ul> element in the html
        return self.soup.find(name="ul").select("li")

    def get_company_name(self):
        company_name_li = self.ul_element[0]  # first <li> element contains the company name
        company_name_span = company_name_li.select("span")[0].select("span")[1].select("span")[0]
        company_name = company_name_span.text.strip()
        return company_name

    def get_location(self):
        location_li = self.ul_element[1]  # second <li> element contains the location
        contract_li = self.ul_element[2]  # third <li> element contains the contract type
        contract_type = contract_li.select("span")[0].select("span")[1].select("span")[0]
        if "remote" in contract_type.text.strip().lower():
            return "Remote"
        location_span = location_li.select("span")[1]
        location = location_span.text.strip().split(" ")[0]  # get only first city name
        return location


class ReedScraper(PageScraper):
    """
    html scraper for pages of the form
        https://www.reed.co.uk/jobs/...
    """
    def __init__(self, url):
        super().__init__(url)
        self.site = "Reed"

    def get_company_name(self):
        posted_by_div = self.soup.select("div[class*='job-title-block_postedBy']")[0]
        if posted_by_div.select("a"):
            company_name = posted_by_div.select("a")[0].text
        else:
            company_name = posted_by_div.text.split("by ")[-1]
        return company_name

    def get_location(self):
        job_metadata_ul = self.soup.select("ul[class^='index-module_jobMetadata']")[0]
        job_metadata_li = job_metadata_ul.select("li")
        # location is always in the 2nd li element
        location = job_metadata_li[1].text.split(",")[0]
        return location

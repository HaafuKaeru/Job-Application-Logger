import requests
from bs4 import BeautifulSoup


# imports for various attempts to try and scrape Indeed.com

# import hrequests
# from selenium import webdriver
# import chromedriver_binary  # Adds chromedriver binary to path
# driver = webdriver.Chrome()
# driver.get("https://www.indeed.com/")


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:157.0) Gecko/20100101 Firefox/157.0"


class PageScraper:
    """
    Template class for other web scraping classes
    Also initialise the SOUP
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

    def get_company_name(self):
        pass

    def get_location(self):
        pass

    def get_position_name(self):
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
        return location

    def get_position_name(self) -> str:
        # first h1 contains position name
        h1_tag = self.soup.find(name="h1")
        position_name = h1_tag.text.strip()
        return position_name


class IndeedScraper(PageScraper):
    """
    html scraper for pages of the form
        https://uk.indeed.com/viewjob?jk=job_listing_id&hl=en

    ***This is currently not working

    TODO: Indeed has a strict security check to prevent scraping

    Failed attempts:
    https://learnwebscraping.substack.com/p/how-i-scraped-indeed-website
    https://daijro.gitbook.io/hrequests
    https://stackoverflow.com/questions/64409393/how-to-get-past-javascript-is-disabled-in-your-browser-error-when-web-scraping-w
    """

    def __init__(self, url):
        super().__init__(url)
        self.site = "Indeed"

    def get_company_name(self):
        pass

    def get_location(self):
        pass

    def get_position_name(self):
        # first h1 contains position name
        h1_tag = self.soup.find(name="h1")
        print(h1_tag)
        print(self.soup.prettify())
        position_name = h1_tag.text.strip()
        return position_name


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

    def get_position_name(self):
        # first h1 contains position name
        h1_tag = self.soup.find(name="h1")
        position_name = h1_tag.text.strip()
        return position_name
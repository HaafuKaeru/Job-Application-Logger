from pprint import pprint
from sheet_manager import SheetManager
from web_scraper import LinkedinScraper, IndeedScraper, TotalJobsScraper, ReedScraper
from date_calculator import DateCalculator


def clean_url(url: str) -> str:
    """
    Removes any GET request parameters
    """
    return url.split("?")[0]


def main():

    print("\nWell done for applying :) Let's update the Google sheet")
    while True:
        input_link = input("Link: ")
        if input_link.lower() == "done":
            print("Keep fighting! ✊")
            break
        elif "http" not in input_link.lower():
            print("Please input a valid link")
            continue

        link = clean_url(input_link)
        if "linkedin" in link:
            page_scraper = LinkedinScraper(link)
        elif "indeed" in link:
            page_scraper = IndeedScraper(link)
        elif "totaljobs" in link:
            page_scraper = TotalJobsScraper(link)
        elif "reed" in link:
            page_scraper = ReedScraper(link)
        else:
            print("Please insert a supported job posting website link\n")
            continue
        company_name = page_scraper.get_company_name()

        yes_no = input("Is this from a recruiting company? yes/no: ")
        is_recruiter = True if "yes" in yes_no.lower() else False

        if is_recruiter:
            company_name = f"N/A [{company_name}]"
        location = page_scraper.get_location()
        position_name = page_scraper.get_position_name()

        date_calculator = DateCalculator()
        date = date_calculator.get_date()

        sheet_manager = SheetManager()
        result = sheet_manager.add_row(
            company_name,
            location,
            position_name,
            date,
            link,
            page_scraper.site
        )
        pprint(result)
        print("")


if __name__ == '__main__':
    main()
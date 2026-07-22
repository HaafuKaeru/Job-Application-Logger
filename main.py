from pprint import pprint
from sheet_manager import SheetManager
from web_scraper import LinkedinScraper, IndeedScraper
from date_calculator import DateCalculator


def main():

    print("\nWell done for applying :) Let's update the Google sheet")
    while True:
        user_input = input("Link: ")
        if user_input.lower() == "done":
            print("Keep fighting! ✊")
            break
        elif "http" not in user_input.lower():
            print("Please input a valid link")
            continue

        if "linkedin" in user_input:
            page_scraper = LinkedinScraper(user_input)
        elif "indeed" in user_input:
            page_scraper = IndeedScraper(user_input)
        else:
            print("Please insert a linkedin or indeed link\n")
            continue
        company_name = page_scraper.get_company_name()

        yes_no = input("Is this from a recruiting company? yes/no: ")
        is_recruiter = True if yes_no.lower() == "yes" else False

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
            user_input,
            page_scraper.site
        )
        pprint(result)

        print("")


if __name__ == '__main__':
    main()
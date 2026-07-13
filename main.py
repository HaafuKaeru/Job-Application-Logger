from pprint import pprint
from sheet_manager import SheetManager
from web_scraper import LinkedinScraper
from date_calculator import DateCalculator


def main():

    print("\nWell done for applying :) Let's update the Google sheet")
    while True:
        user_input = input("Link: ")
        if user_input.lower() == "exit":
            print("Keep fighting! ✊")
            break
        yes_no = input("Is this from a recruiting company? yes/no: ")
        is_recruiter = True if yes_no.lower() == "yes" else False

        linkedin_scraper = LinkedinScraper(user_input)
        company_name = linkedin_scraper.get_company_name()
        if is_recruiter:
            company_name = f"N/A [{company_name}]"
        location = linkedin_scraper.get_location()
        position_name = linkedin_scraper.get_position_name()

        date_calculator = DateCalculator()
        date = date_calculator.get_date()

        sheet_manager = SheetManager()
        result = sheet_manager.add_row(
            company_name,
            location,
            position_name,
            date,
            user_input,
            linkedin_scraper.site
        )

        pprint(result)
        print("")


if __name__ == '__main__':
    main()
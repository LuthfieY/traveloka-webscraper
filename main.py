from os import system, environ
from web_scraper import (
    open_webpage,
    wait_for_element,
    next_page,
    explicit_wait,
    change_language,
    get_total_page,
)
from process_data import initialize_datastore_client
from extract_data import extract_hotel_data, extract_and_export_review_data
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def clear_screen():
    system("cls")


def main():
    load_dotenv()
    clear_screen()
    credentials_file = environ.get("CRED_PATH")
    client = initialize_datastore_client(credentials_file)
    url = environ.get("URL")

    driver = open_webpage(url)
    wait_for_element(driver, "div.css-1dbjc4n.r-b83rso.r-f4gmv6", 30)
    source = driver.page_source
    page_content = BeautifulSoup(source, "lxml")

    hotel_data = extract_hotel_data(page_content, client)
    change_language(driver)
    client.put(hotel_data)
    total_page = get_total_page(page_content)
    for i in range(total_page):
        extract_and_export_review_data(page_content, client, hotel_data)
        next_page(driver)
        explicit_wait(driver, 3)
        source = driver.page_source
        page_content = BeautifulSoup(source, "lxml")
        print(f"Page {i+1} has been extracted")

    query = client.query(kind="Review")
    count = len(list(query.fetch()))
    print(f"Total entities: {count}")


if __name__ == "__main__":
    main()

from os import system, environ
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from rich.console import Console
from web_scraper import (
    open_webpage,
    wait_for_element,
    next_page,
    explicit_wait,
    change_language,
    get_total_page,
)
from process_data import initialize_datastore_client
from extract_data import extract_hotel_data, extract_review_data

def clear_screen():
    system("cls")


def main():
    console = Console()
    load_dotenv()
    clear_screen()
    credentials_file = environ.get("CRED_PATH")
    client = initialize_datastore_client(credentials_file)
    url = environ.get("URL")

    driver = open_webpage(url)
    wait_for_element(driver, "div.css-1dbjc4n.r-b83rso.r-f4gmv6", 30)
    source = driver.page_source
    page_content = BeautifulSoup(source, "lxml")
    
    with console.status("[bold green]Changing language...") as status:
        change_language(driver)
        console.log("Language has been change to Bahasa Indonesia")
    
    with console.status("[bold green]Extracting hotel data...") as status:
        hotel_data = extract_hotel_data(url, page_content, client)
        console.log(f"Hotel data has been extracted: {hotel_data['name']}")
    
    total_page = get_total_page(page_content)
    with console.status("[bold green]Extracting review data...") as status:
        for i in range(total_page):
            extract_review_data(page_content, client, hotel_data)
            next_page(driver)
            explicit_wait(driver, 3)
            source = driver.page_source
            page_content = BeautifulSoup(source, "lxml")
            console.log(f"Review data has been extracted: {i+1}/{total_page}")
        
        console.log('[bold][red]Done!')

    query = client.query(kind="Hotel")
    count = len(list(query.fetch()))
    console.log(f"Total hotels: {count}")
    query = client.query(kind="Review")
    count = len(list(query.fetch()))
    console.log(f"Total reviews: {count}")
    driver.quit()


if __name__ == "__main__":
    main()

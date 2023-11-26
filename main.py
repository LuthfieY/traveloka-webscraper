from os import system, environ
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from rich.console import Console
import typer
from WebPageAutomation import (
    open_webpage,
    wait_for_element_css,
    next_page,
    change_language,
)
from DatastoreUtils import initialize_datastore_client
from DataExtraction import extract_hotel_data, extract_review_data, get_total_page

app = typer.Typer()

def clear_screen():
    system("cls")

@app.command()
def main(url: str):
    console = Console()
    load_dotenv()
    clear_screen()
    credentials_file = environ.get("CRED_PATH")
    client = initialize_datastore_client(credentials_file)

    driver = open_webpage(url)
    wait_for_element_css(driver, "div.css-1dbjc4n.r-b83rso.r-f4gmv6", 30)
    source = driver.page_source
    page_content = BeautifulSoup(source, "lxml")

    with console.status("[bold green]Changing language..."):
        change_language(driver)
        console.log("Language has been changed to Bahasa Indonesia")

    with console.status("[bold green]Extracting hotel data..."):
        hotel_data = extract_hotel_data(url, page_content, client)
        console.log(f"Hotel data has been extracted: {hotel_data['name']}")

    total_page = get_total_page(page_content)
    with console.status("[bold green]Extracting review data..."):
        for i in range(total_page):
            extract_review_data(page_content, client, hotel_data)
            console.log(f"Review data has been extracted: page {i+1}/{total_page}")
            if i == total_page - 1:
                break
            next_page(driver)
            wait_for_element_css(driver, "div.css-1dbjc4n.r-14lw9ot.r-h1746q.r-kdyh1x.r-d045u9.r-18u37iz.r-1fdih9r.r-1udh08x.r-d23pfw", 30)
            source = driver.page_source
            page_content = BeautifulSoup(source, "lxml")

        console.log('[bold][red]Done!')

    driver.quit()
    query = client.query(kind="Hotel")
    count = len(list(query.fetch()))
    console.log(f"Total hotels: {count}")
    query = client.query(kind="Review")
    count = len(list(query.fetch()))
    console.log(f"Total reviews: {count}")


if __name__ == "__main__":
    app()

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_webpage(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--log-level=3')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    return driver


def next_page(driver):
    try:
        nextPageButton = wait_for_element(
            driver, '[data-testid="undefined-nextPage"]', timeout=10
        )
        driver.execute_script("arguments[0].click();", nextPageButton)
    except Exception as e:
        print(e)


def wait_for_element(driver, selector, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))


def wait_for_element_xpath(driver, path, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located((By.XPATH, path)))


def explicit_wait(driver, times=5):
    WebDriverWait(driver, times)
    time.sleep(times)


def scroll_to_percentage(driver, percentage):
    # Calculate the scroll position based on the page's height
    page_height = driver.execute_script(
        "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"
    )
    scroll_position = (page_height * percentage) / 100

    # Scroll to the calculated position
    driver.execute_script("window.scrollTo(0, arguments[0]);", scroll_position)


def scroll_to_element_with_percentage(driver, element, percentage):
    # Scroll to the element using JavaScript
    driver.execute_script("arguments[0].scrollIntoView();", element)

    # Get the viewport height (the height of the visible area)
    viewport_height = driver.execute_script("return window.innerHeight;")

    # Calculate the desired scroll position based on the percentage
    scroll_position = element.location["y"] - (percentage * viewport_height)

    # Scroll to the calculated position using JavaScript
    driver.execute_script("window.scrollTo(0, arguments[0]);", scroll_position)


def zoom_out(driver, percentage):
    driver.execute_script(f"document.body.style.zoom = '{percentage}'")


def change_language(driver):
    explicit_wait(driver, 3)
    above_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "div.css-901oao.r-cwxd7f.r-aka4e8.r-t1w4ow.r-1b43r93.r-majxgm.r-rjixqe.r-ytfskt.r-fdjqy7.r-1vzi8xi",
            )
        )
    )
    dropdowns = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.css-1dbjc4n.r-tqpus0")
        )
    )

    dropdown = dropdowns[-1]
    driver.execute_script("arguments[0].scrollIntoView();", above_dropdown)
    dropdown.click()
    explicit_wait(driver, 1)
    languages = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                "div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1e081e0.r-5njf8e",
            )
        )
    )
    bahasa_indonesia = languages[1]
    bahasa_indonesia.click()


def is_element_clickable(driver, selector):
    try:
        wait_for_element(driver, selector, 10)
        return True
    except Exception:
        return False


def get_total_page(page_content):
    page_nums = page_content.find_all(
        "div",
        class_="css-901oao css-bfa6kz r-1i6uqv8 r-t1w4ow r-cygvgh r-b88u0q r-1iukymi r-q4m81j",
    )
    if(len(page_nums) == 0):
        return 1
    total_page = page_nums[-1]
    return int(total_page.text)
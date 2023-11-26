from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def handle_exception(driver, error_message):
    print(f"An error occurred: {error_message}. Quitting the driver...")
    driver.quit()

def open_webpage(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.maximize_window()
        driver.get(url)
    except WebDriverException as e:
        print(f"An error occurred: {e}")
        driver.quit()
    return driver


def next_page(driver):
    try:
        next_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    '[data-testid="undefined-nextPage"]',
                )
            )
        )
        next_page_button.click()
    except TimeoutException:
        handle_exception(driver, "Next page button not found within the specified time.")


def wait_for_element_css(driver, selector, timeout=10):
    try:
        wait = WebDriverWait(driver, timeout)
    except TimeoutException:
        handle_exception(driver, "TimeoutException: Element not found within the specified time.")
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))


def change_language(driver):
    above_dropdown = wait_for_element_css(
        driver,
        "div.css-901oao.r-cwxd7f.r-aka4e8.r-t1w4ow.r-1b43r93.r-majxgm.r-rjixqe.r-ytfskt.r-fdjqy7.r-1vzi8xi",
    )
    try:
        dropdowns = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.css-1dbjc4n.r-tqpus0")
            )
        )
    except TimeoutException:
        handle_exception(driver, "TimeoutException: Dropdowns not found within the specified time.")
    except WebDriverException as e:
        handle_exception(driver, e)

    language_dropdown = dropdowns[-1]
    driver.execute_script("arguments[0].scrollIntoView();", above_dropdown)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "div.css-1dbjc4n.r-tqpus0",
                )
            )
        )
        language_dropdown.click()
    except TimeoutException:
        handle_exception(driver, "TimeoutException: Language dropdown not found within the specified time.")
    except WebDriverException as e:
        handle_exception(driver, e)

    try:
        languages = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    "div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1e081e0.r-5njf8e",
                )
            )
        )
    except TimeoutException:
        handle_exception(driver, "TimeoutException: Languages not found within the specified time.")
    except WebDriverException as e:
        handle_exception(driver, e)

    bahasa_indonesia = languages[1]
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1e081e0.r-5njf8e",
                )
            )
        )
        bahasa_indonesia.click()
    except TimeoutException:
        handle_exception(driver, "TimeoutException: Bahasa Indonesia not found within the specified time.")
    except WebDriverException as e:
        handle_exception(driver, e)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver for the browser u are using
driver = webdriver.Firefox()

# list of traders (for now just testing on 1 trader
traders = "https://www.tradingview.com/u/AlanSantana/"
# list of the symbols from the top 20 crypto coins based on market cap (excluding stable coins)
crypto_list = ["BTC", "ETH", "BNB", "SOL", "XRP", "DOGE", "TON", "ADA", "AVAX", "SHIB", "TRX", "DOT", "BCH", "LINK", "MATIC", "NEAR", "LTC",
               "ICP", "LEO", "DAI"]

# open the page of the traders (this will eventually be a loop of all the traders)
driver.get(traders)
time.sleep(5)

# Find the ideas tab
ideas = driver.find_elements(By.CSS_SELECTOR,
                             'div.js-card-list.tv-card-container__ideas > '
                             'div.tv-feed__item.tv-feed-layout__card-item.js-feed__item--inited')

# Loop through the ideas
for i in range(min(10, len(ideas))):
    # reload the ideas (addresses stale element issues) # problem fixed with the use of ChatGPT
    ideas = driver.find_elements(By.CSS_SELECTOR,
                                 'div.js-card-list.tv-card-container__ideas > '
                                 'div.tv-feed__item.tv-feed-layout__card-item.js-feed__item--inited')

    # open the page and wait until its fully loaded
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ideas[i])).click()
    time.sleep(5)

    # check the symbol of the idea to see if its crypto related
    symbol_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "tv-chart-view__symbol-link"))

    )
    href_symbol = symbol_element.get_attribute("href")
    if any(symbol in href_symbol for symbol in crypto_list):
        # Extract all the text, excluding the pictures
        detailed_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.tv-chart-view__section.tv-chart-view__section--with-separator"))
        ).text

        # Print the extracted text
        print(f"Idea {i + 1} Details:")
        print(detailed_text)
        print("-" * 50)
    else:
        print(f"Idea {i + 1} is not related to the specified cryptocurrencies.")
    # Go back to the idea page
    driver.back()
    # wait a little bit so that the page is fully loaded
    time.sleep(5)

# Close the browser
driver.quit()

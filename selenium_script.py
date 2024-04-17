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

# Initialize the counters
counter_crypto_idea = 0
counter_ideas = 0

# Loop through the ideas
while counter_crypto_idea < 10:
    # Locate all ideas on the page at this moment
    ideas = driver.find_elements(By.CSS_SELECTOR,
                                 'div.js-card-list.tv-card-container__ideas > div.tv-feed__item.tv-feed-layout__card-item.js-feed__item--inited')

    # Click on the current idea
    ideas[counter_ideas].click()
    time.sleep(5)

    # Check the href attribute of the cryptocurrency symbol link
    try:
        symbol_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "tv-chart-view__symbol-link"))
        )
        href_attribute = symbol_link.get_attribute('href')

        # Continue only if the href contains one of the specified cryptocurrency symbols
        if any(symbol in href_attribute for symbol in crypto_list):
            detailed_text = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "tv-chart-view__section--with-separator"))
            ).text
            print(f"Crypto Idea {counter_crypto_idea + 1} Details:")
            print(detailed_text)
            print("-" * 50)

            # Increment the crypto-related idea count
            counter_crypto_idea += 1

        # Navigate back to the ideas list
        driver.back()
        time.sleep(5)
        counter_ideas += 1  # Move to the next idea

    except Exception as e:
        print(f"An error occurred while processing idea: {str(e)}")
        driver.back()
        time.sleep(5)
        counter_ideas += 1  # Skip to the next idea in case of an error

# Close the browser
driver.quit()

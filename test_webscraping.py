import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver for the browser u are using
driver = webdriver.Firefox()

# list of traders
traders = ["https://www.tradingview.com/u/AlanSantana/"]
# list of the symbols from the top 20 crypto coins based on market cap (excluding stable coins)
crypto_list = ["BTC", "ETH", "BNB", "SOL", "XRP", "DOGE", "TON", "ADA", "AVAX", "SHIB", "TRX", "DOT", "BCH", "LINK", "MATIC", "NEAR", "LTC",
               "ICP", "LEO", "DAI"]

# Test for 1 trader
for trader in traders:
    driver.get(trader)
    time.sleep(5)

    # name and path of dataset
    trader_name = trader.split("/")[-2]
    file_name = trader_name + "ideas.txt"
    file_path = os.path.join("Dataset_test", file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        # Initialize the counters
        counter_crypto_idea = 0
        counter_ideas = 0

        # Loop through the ideas
        while counter_crypto_idea < 10:
            # Wait until the ideas are definitely loaded on the page
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'div.tv-card-container > div.tv-card-container__columns > div.js-card-list.tv-card-container__ideas > '
                                      'div.tv-feed__item.tv-feed-layout__card-item.js-feed__item--inited')))
            # Locate all ideas on the page at this moment
            ideas = driver.find_elements(By.CSS_SELECTOR,
                                         'div.tv-card-container > div.tv-card-container__columns > div.js-card-list.tv-card-container__ideas > '
                                         'div.tv-feed__item.tv-feed-layout__card-item.js-feed__item--inited')
            if counter_ideas >= len(ideas):
                # click the load more button at the bottom of the ideas
                try:
                    load_more_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.tv-load-more__btn.js-load-more.tv-button--loader'))
                    )
                    load_more_button.click()
                    # Wait for new ideas to load
                    time.sleep(5)
                    # Refresh the list of ideas
                    ideas = driver.find_elements(By.CSS_SELECTOR,
                                                 'div.js-card-list.tv-card-container__ideas > '
                                                 'div.tv-feed__item.tv-feed-layout__card-item.js-feed__item--inited')
                except Exception as e:
                    print("No more ideas to load or failed to load more ideas:", str(e))
                    break

            # Click on current Idea and wait until everything is loaded
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ideas[counter_ideas])).click()
            time.sleep(5)
            # Check the href attribute of the cryptocurrency symbol link
            try:
                symbol_link = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "tv-chart-view__symbol-link"))
                )
                href_attribute = symbol_link.get_attribute('href')
                # print(href_attribute)
                crypto_symbol = href_attribute.split("/")[-2]
                # print(href_attribute.split("/"))
                first_half = (int((len(crypto_symbol) / 2 + 0.5)) + 1)
                href = crypto_symbol[:first_half]
                # Continue only if the href contains one of the specified cryptocurrency symbols
                if any(symbol in href for symbol in crypto_list):
                    detailed_text = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "tv-chart-view__section--with-separator"))
                    ).text
                    file.write(f"Crypto Idea {counter_crypto_idea + 1} Details for {trader_name}:\n{detailed_text}\n{'-' * 50}\n")

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

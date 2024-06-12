# import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

# Initialize the WebDriver for the browser u are using
driver = webdriver.Firefox()

# list of traders
traders = ["https://www.tradingview.com/u/CRYPTOMOJO_TA/"]
# list of the symbols from the top 20 crypto coins based on market cap (excluding stable coins)
crypto_list = ["BTC", "ETH", "BNB", "SOL", "XRP", "DOGE", "TON", "ADA", "AVAX", "SHIB", "TRX", "DOT", "BCH", "LINK", "MATIC", "NEAR", "LTC",
               "ICP", "LEO", "DAI"]

# Test for 1 trader
for trader in traders:
    driver.get(trader)
    time.sleep(5)

    # name and path of dataset
    # trader_name = trader.split("/")[-2]
    # file_name = trader_name + "ideas.txt"
    # file_path = os.path.join("Dataset_test", file_name)
    # with open(file_path, "w", encoding="utf-8") as file:
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
                idea_title = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.tv-chart-view__title-name-wrap > "
                                                                       "h1.tv-chart-view__title-name.js-chart-view__name"))).text
                idea_timestamp_location = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.tv-chart-view__title-time")))
                idea_timestamp = idea_timestamp_location.get_attribute("data-timestamp")
                print(f"Crypto Idea {counter_crypto_idea + 1} Details:")
                print("Title: ", idea_title)
                print("Timestamp: ", idea_timestamp)
                if idea_timestamp is None:
                    try:
                        updates_locations = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.tv-chart-updates.js-chart-updates"))
                        )

                        initial_post = updates_locations.find_element(By.CSS_SELECTOR,
                                                              "div.tv-chart-updates__entry.tv-chart-updates__entry--initial.js-chart-update__entry")
                        initial_post_timestamp = initial_post.find_element(By.CSS_SELECTOR, "span.tv-chart-updates__update-time").get_attribute(
                            "data-timestamp")
                        initial_post_text = initial_post.find_element(By.CSS_SELECTOR, "div.tv-chart-updates__body").text
                        print("initial post timestamp:\n" + initial_post_timestamp)
                        print("initial post:\n" + initial_post_text)
                        updates_posts = updates_locations.find_elements(By.CSS_SELECTOR,
                                                       "div.tv-chart-updates__entry.tv-chart-updates__entry--comment.js-chart-update__entry")
                        update_count = 0
                        for update in updates_posts:
                            update_count += 1
                            update_timestamp = update.find_element(By.CSS_SELECTOR, "span.tv-chart-updates__update-time").get_attribute("data-timestamp")
                            update_text = update.find_element(By.CSS_SELECTOR, "div.tv-chart-updates__body").text
                            print("update", update_count)
                            print("update post timestamp:\n" + update_timestamp)
                            print("update post text:\n" + update_text)
                    except NoSuchElementException as e:
                        print("element not found")
                else:
                    idea_description = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.tv-chart-view__description.selectable"))).text
                    print("idea description:", idea_description)
                counter_crypto_idea += 1
            # Navigate back to the ideas list
            driver.back()
            time.sleep(5)
            counter_ideas += 1  # Move to the next idea

        except Exception as e:
            # print(f"An error occurred while processing idea: {str(e)}")
            driver.back()
            time.sleep(5)
            counter_ideas += 1  # Skip to the next idea in case of an error

# Close the browser
driver.quit()

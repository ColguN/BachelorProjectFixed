import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

# Initialize the WebDriver for the browser u are using
driver = webdriver.Firefox()

# list of traders
traders = ["https://www.tradingview.com/u/CryptoColugo/"]
# list of the symbols from the top 20 crypto coins based on market cap (excluding stable coins)
crypto_list = ["BTC", "ETH", "BNB", "SOL", "XRP", "DOGE", "TON", "ADA", "AVAX", "SHIB", "TRX", "DOT", "BCH", "LINK", "MATIC", "NEAR", "LTC",
               "ICP", "LEO", "DAI"]
name_of_trader = []
post_title = []
post_length = []
post_type = []
post_text = []
post_timestamp = []

# Test for 1 trader
for trader in traders:
    driver.get(trader)
    time.sleep(5)

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
                        post_type.append("Initial post")  # add post type to list
                        post_timestamp.append(initial_post_timestamp)
                        post_text.append(initial_post_text)
                        print("initial post:\n" + initial_post_text)
                        updates_posts = updates_locations.find_elements(By.CSS_SELECTOR,
                                                       "div.tv-chart-updates__entry.tv-chart-updates__entry--comment.js-chart-update__entry")
                        update_count = 0
                        for update in updates_posts:
                            update_count += 1
                            post_type.append(f"Update post {update_count}")
                            update_timestamp = update.find_element(By.CSS_SELECTOR, "span.tv-chart-updates__update-time").get_attribute("data-timestamp")
                            post_timestamp.append(update_timestamp)
                            update_text = update.find_element(By.CSS_SELECTOR, "div.tv-chart-updates__body").text
                            post_text.append(update_text)
                            print("update", update_count)
                            print("update post timestamp:\n" + update_timestamp)
                            print("update post text:\n" + update_text)
                        for _ in range(update_count + 1):
                            post_length.append(update_count + 1)
                            post_title.append(idea_title)
                    except NoSuchElementException as e:
                        print("element not found")
                else:
                    post_timestamp.append(idea_timestamp)
                    post_length.append(1)
                    post_title.append(idea_title)
                    post_type.append("Initial post")
                    idea_description = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.tv-chart-view__description.selectable"))).text
                    post_text.append(idea_description)
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

trader_name = traders[0].split("/")[-2]
for _ in range(len(post_text)):
    name_of_trader.append(trader_name)

print(len(name_of_trader), name_of_trader)
print(len(post_title), post_title)
print(len(post_length), post_length)
print(len(post_timestamp), post_timestamp)
print(len(post_type), post_type)
print(len(post_text))

data = {"Trader": name_of_trader,
        "Title": post_title,
        "Post length": post_length,
        "Post type":post_type,
        "Timestamp": post_timestamp,
        "Text": post_text}
df = pd.DataFrame(data)

csv_file_path = os.path.join("Dataset_test", f"{trader_name}.csv")

df.to_csv(csv_file_path, index=False, encoding="utf-8")

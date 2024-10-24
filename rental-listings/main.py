from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeuvvAf-8LXwXzFpyQ-tvgnuBPMWTCfHd1XMcjAeBYJOEK59w/viewform?usp=sf_link"

response = requests.get(ZILLOW_URL)
soup = BeautifulSoup(response.text, "html.parser")

all_prices = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
all_links = soup.find_all(class_="StyledPropertyCardDataArea-anchor")

# Gets the price, link, and address of every listing
prices = [price.getText().split("+")[0].split("/")[0] for price in all_prices]
links = [link.get("href") for link in all_links]
addresses = [link.find(name="address").getText().split("|")[-1].strip() for link in all_links]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)
driver.get(FORM_URL)

# Fills out Google Form with fetched rent data
for i in range(len(prices)):
    all_inputs = driver.find_elements(By.CLASS_NAME, "whsOnd.zHQkBf")
    address = all_inputs[0]
    price = all_inputs[1]
    link = all_inputs[2]
    submit_button = driver.find_element(By.CLASS_NAME, "uArJ5e.UQuaGc.Y5sE8d.VkkpIf.QvWxOd")
    sleep(1)
    address.send_keys(addresses[i])
    price.send_keys(prices[i])
    link.send_keys(links[i])
    submit_button.click()
    sleep(1)
    submit_again = driver.find_element(By.LINK_TEXT, "Submit another response")
    submit_again.click()

driver.quit()

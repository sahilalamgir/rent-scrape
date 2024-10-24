import requests
from bs4 import BeautifulSoup

ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(ZILLOW_URL)
soup = BeautifulSoup(response.text, "html.parser")

all_prices = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
all_links = soup.find_all(class_="StyledPropertyCardDataArea-anchor")

# Gets the price, link, and address of every listing
prices = [price.getText().split("+")[0].split("/")[0] for price in all_prices]
links = [link.get("href") for link in all_links]
addresses = [link.find(name="address").getText().split("|")[-1].strip() for link in all_links]

print(prices)
print(links)
print(addresses)

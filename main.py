import time

from bs4 import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from pprint import pprint

google_doc_url = "https://docs.google.com/forms/d/e/1FAIpQLSePnSVNNwCXrUVM-P-vRzFALSGXFa36imB6oeZGJ8lwH6EwnQ/viewform?usp=sf_link"

url = "https://appbrewery.github.io/Zillow-Clone/"
response = requests.get(url=url)
file = response.text
soup = BeautifulSoup(file, "html.parser")
select_link = soup.select(selector="ul li div a")

link_list = [item.get_attribute_list("href") for item in select_link]
link_list = link_list[::2]

price_list = soup.find_all("span", attrs={'data-test': "property-card-price"})
all_prices = []

for item in price_list:
    price = item.text.split("/")
    new_price = (int(price[0].split("+")[0].replace("$","").replace(",","")))
    all_prices.append(new_price)
print(all_prices)
all_addresses = soup.select(selector="a address")

new_address_list = [item.get_text().strip() for item in all_addresses]


my_listing_dictionary = {}
for index in range(len(link_list)):
    my_listing_dictionary[new_address_list[index]] = {"price": all_prices[index],
                                                      "link": link_list[index]}

print(my_listing_dictionary)

keep_open = webdriver.ChromeOptions()
keep_open.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=keep_open)
driver.get(url=google_doc_url)
time.sleep(2)

for key in my_listing_dictionary:

    question_1 = driver.find_element(By.XPATH,
                                     value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    question_2 = driver.find_element(By.XPATH,
                                     value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input ')
    question_3 = driver.find_element(By.XPATH,
                                     value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.CSS_SELECTOR, value=".NPEfkd")
    time.sleep(1)
    question_1.send_keys(key)
    question_2.send_keys(my_listing_dictionary[key]['price'])
    question_3.send_keys(my_listing_dictionary[key]['link'])
    submit.click()
    time.sleep(2)
    submit_another = driver.find_element(By.CSS_SELECTOR, value="div div div div a")
    submit_another.click()


from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import requests
from bs4 import BeautifulSoup
from time import sleep

driver = webdriver.Firefox()
driver.get("https://rumble.com/v2vyfpm-rt-news-livestream-247.html")

sleep(3)

# V1.0 (beta)
# Currently only scrapes historical messages

# TODO: 
# Add live comment scraping
# Add additional args (time to scrape for?, include historical comments?)

soup = BeautifulSoup(driver.page_source, 'html.parser')

messages = soup.find_all('div', class_="chat-history--message")

for message in messages:
	print(message.get_text())

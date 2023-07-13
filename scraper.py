from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options 
import requests
from bs4 import BeautifulSoup
from time import sleep
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("URL", help="URL of a Rumble live stream")
args = parser.parse_args()

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get(args.URL)

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

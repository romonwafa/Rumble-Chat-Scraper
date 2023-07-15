from selenium import webdriver
from selenium.webdriver.firefox.options import Options 
from bs4 import BeautifulSoup
from time import sleep
import argparse
import csv


# Initialize arguments parser
parser = argparse.ArgumentParser()
parser.add_argument('URL', help='URL of a Rumble live stream')
parser.add_argument('-o', '--filename', nargs='?', default=None, help='output CSV file')
args = parser.parse_args()

# Initialize Selenium
options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
driver.get(args.URL)

# Wait for chats to load
print("Scraping live chats...\n")
sleep(3)

# Nest message lists into one big list
messages_list = []

soup = BeautifulSoup(driver.page_source, 'html.parser')
chat_history = soup.find('div', class_='chat-history')
try:
	messages = chat_history.find_all('li', class_='chat-history--row')
except AttributeError:
	print('Channel is not live.')
	driver.quit()
	quit()

# Quit driver
driver.quit()

# Scrape messages
for message in messages:
	# True when message is a rant message
	is_rant = False
	# Create list to store information about each message
	message_data = []

	# Get user id
	userid = message['data-message-user-id']
	# Get message id
	messageid = message['data-message-id']
	# Get user avatar (TypeError exception occurs if user has no avatar image)
	try:
		avatar = message.find('img', class_='chat-history--user-avatar')
		avatar_url = avatar['src']
	except TypeError:
		avatar_url = ''
	
	# Note! AttributeError exceptions occur on rant messages (they don't)
	# TODO: Handle rant chats properly
	try:
		# Get message wrapper
		# Need to handle this properly...
		message_wrapper = message.find('div', class_='chat-history--message-wrapper')
			
		# Get username
		username_div = message_wrapper.find('div', class_='chat-history--username')
		username_hyperlink = username_div.find('a')
		username = username_hyperlink.get_text()
		# Get profile URL
		profile_url = username_hyperlink['href']
		# Get message text
		message_text = message_wrapper.find('div', class_='chat-history--message').get_text()

		# Append message information to a list
		message_data.append(userid)
		message_data.append(messageid)
		message_data.append(avatar_url)
		message_data.append(profile_url)
		message_data.append(username)
		message_data.append(message_text)
		print(message_data)
		# Append message_data to messages_list
		messages_list.append(message_data)
	except AttributeError:
		pass

# Write .csv file
if args.filename is not None:
	fields = ['User ID', 'Message ID', 'Avatar URL', 'Profile URL', 'Username', 'Message Text']
	with open(args.filename, 'w') as f:
		write = csv.writer(f)
		write.writerow(fields)
		write.writerows(messages_list)
	print(f"\nExported {args.filename}\n")
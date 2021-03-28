from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import datetime
import time
import re
from ordered_set import OrderedSet

# start time
start_time = datetime.datetime.now()
today = datetime.date.today()

# dd/mm/YY
date = today.strftime("%d-%m-%Y")

# read topics form a file
file_question_topics = open("topic_list.txt", mode='r', encoding='utf-8')
topics = file_question_topics.readlines()

for topic in topics:

	# instantiate a chrome options object so you can set the size and headless preference
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument(" --window-size=1920x1080")

	chrome_driver = os.getcwd() +"/chromedriver"

	# Set the browser settings to web driver
	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

	url = "https://nl.quora.com/search?q="+topic+"&type=question"
	print("Search questions for: ", url)
	driver.get(url)

	# define pause time for browser
	SCROLL_PAUSE_TIME = 3

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	# infinite while loop, break it when you reach the end of the page or not able to scroll further.
	while True:
		html_source = " "
		i = 0

		# try to scroll 5 times in case of slow connection
		while i < 5:

			# Scroll down to one page length
			driver.execute_script("window.scrollBy(0, 1080);")

			# Wait to load page
			time.sleep(SCROLL_PAUSE_TIME)
			# get page height in pixels
			new_height = driver.execute_script("return document.body.scrollHeight")

			# break this loop when you are able to scroll further
			if new_height != last_height:
				break
			i += 1

		# get html page source
		html_source = driver.page_source
		# Regex to find questions: https://nl.quora.com/some-question
		regex_Qs = r"https:\/\/nl\.quora\.com\/[A-Z][A-Za-zÀ-ž0-9\%\\u0370-\\u03FF\\u0400\-\\u04FF]+[A-Za-zÀ-ž0-9]"

		matches = re.findall(regex_Qs, html_source, re.MULTILINE)
		unique_questions = OrderedSet()
		for match in matches:
			clean_match = match.split('?')[0]
			unique_questions.add(clean_match)

		time.sleep(SCROLL_PAUSE_TIME)
		# not able to scroll further, break the infinite loop
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height


	# write content of set to a file called question_urls_date.csv
	questions_directory = 'questions'
	os.makedirs('questions', exist_ok=True)
	file_name = questions_directory + '/' + topic + '_question_urls_'+date+'.csv'
	file_question_urls = open(file_name, mode='w', encoding='utf-8')
	for question in unique_questions:
		link_url = question
		print(link_url)
		file_question_urls.write(question + "\n")
	file_question_urls.close()
	print('quitting chrome')
	driver.quit()

# finish time
end_time = datetime.datetime.now()
print(end_time-start_time)

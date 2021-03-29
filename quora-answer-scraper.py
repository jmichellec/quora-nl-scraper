import datetime
from selenium.webdriver.chrome.options import Options
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from ordered_set import OrderedSet

# Fill in date of search
date = '28-03-2021'
# start time
start_time = datetime.datetime.now()

# read topics form a file
file_question_topics = open("topic_list.txt", mode='r', encoding='utf-8')
topics = file_question_topics.readlines()

for topic in topics:
	# read questions form files under questions directory
	questions_file = topic + '_question_urls_'+date+'.csv'
	questions = open('questions/'+ questions_file, mode='r', encoding='utf-8')
	# write contents of set to a file called answers.csv
	answers_directory = 'answers'
	os.makedirs('answers', exist_ok=True)
	file_name = answers_directory + '/' + topic +'_'+date+ '_answers.csv'
	f = open(file_name, mode='a', encoding='utf-8')
	f.write('question'+'\t'+'user_bio'+'\t'+'text'+'\n')

	for question in questions:
		question = question.rstrip()
		print('Question: ', question)
		# instantiate a chrome options object so you can set the size and headless preference
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument(" --window-size=1920x1080")

		# download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads
		# and put it in the current directory
		chrome_driver = os.getcwd() + "/chromedriver"

		# Set the browser settings to web driver
		driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

		# give the url to scrap
		driver.get(question)

		# define pause time for browser
		SCROLL_PAUSE_TIME = 3

		# get browser source
		html_source = driver.page_source
		question_count_soup = BeautifulSoup(html_source, 'html.parser')

		# Get scroll height
		last_height = driver.execute_script("return document.body.scrollHeight")
		answer_set = OrderedSet()

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
			soup = BeautifulSoup(html_source, 'html.parser')

			# get answers
			answer_texts = soup.find_all('div', attrs={'class': 'q-relative spacing_log_answer_content puppeteer_test_answer_content'})
			# get occupation/bio description
			users = soup.find_all('span', attrs={'class': 'CssComponent-sc-1oskqb9-0 AbstractSeparatedItems___StyledCssComponent-sc-46kfvf-0 bxBZxD'})
			user_bios = []
			for i in range(len(users)-1):

				# css finds weergaven too, remove those
				if 'weergaven' not in users[i].text:
					user_bio = users[i].find('span', attrs={'class': 'q-text qu-borderWidth--retinaOverride qu-borderWidth--regular'})
					if user_bio == None:
						user_bio = 'None'
					else:
						user_bio = user_bio.text
					user_bios.append(user_bio)

			for i, answer in enumerate(answer_texts):
				# clean_paragraphs = []
				paragraphs = answer.find_all(text=True)

				# Bit of cleaning to fit the csv
				# Code
				print(user_bios[i])
				print("".join(paragraphs))

				answer_set.add((user_bios[i], "".join(paragraphs)))
			# not able to scroll further, break the infinite loop
			new_height = driver.execute_script("return document.body.scrollHeight")
			if new_height == last_height:
				break
			last_height = new_height

			print('Total Answers: ' + str(len(answer_set)))

		# Write to csv
		for answer in answer_set:
			# question, user_bio, answer
			f.write(question+'\t'+answer[0]+'\t'+answer[1]+'\n')
		print('quitting chrome')
		driver.quit()
	f.close()


# finish time
end_time = datetime.datetime.now()
print(end_time-start_time)
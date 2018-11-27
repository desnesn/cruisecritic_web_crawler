#!/usr/bin/python

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/

import csv
import html
import urllib2

from bs4 import BeautifulSoup

##############################
####### USER VARIABLES #######
##############################

# SET PORT NAME
port = "shanghai"
#port = "beijing"

# SET VERBOSE
verbose = 1
#verbose = 0

#BUG ON THE SITE FOR NOT SHOWING BUBBLE REVIEWS ON THE LAST PAGE
page_limit = 7

#############################
#############################
#############################

url = "https://www.cruisecritic.com/memberreviews/ports/" + port + "-cruises/"

user = 1

page_cnt = 1

f = open(port + '_feedbacks.csv', 'w')

while True:

	page = urllib2.urlopen(url)

	if( ( page.getcode() == 200 ) and (page_cnt <= page_limit) ):

		soup = BeautifulSoup(page, "lxml")

		feedbacks = soup.find_all('a', class_="chevron-after")

		for feed in feedbacks:
			user_link = "https://www.cruisecritic.com" + feed.get("href")
		    
			user_page = urllib2.urlopen(user_link).read()

			user_soup = BeautifulSoup(user_page, "lxml")

			user_details = user_soup.find_all('div',class_='review-author-details')

			user_date = user_soup.find_all('div',class_='heading__heavy--sm')
			
			if verbose:
				print "==========================="
				print "User " + str(user) + " review:"
				print "==========================="

				print user_details[0].span.text.strip()
				print user_details[0].div.div.text.strip()
				print user_details[0].div.div.findNext().div.text.strip()
				print user_date[0].findNext().li.text.strip()
				print user_details[0].div.div.findNext().div.findNext().text.strip()

			f.write(user_details[0].span.text.encode('utf-8').strip() + '\n')
			f.write(user_details[0].div.div.text.encode('utf-8').strip() + '\n')
			f.write(user_details[0].div.div.findNext().div.text.encode('utf-8').strip() + '\n')
			f.write(user_date[0].findNext().li.text.encode('utf-8').strip() + '\n')
			f.write(user_details[0].div.div.findNext().div.findNext().text.encode('utf-8').strip() + '\n')

			user_feedbacks = user_soup.find_all('li',class_='member-review__port-list-item')
		   
			for user_feed in user_feedbacks:
				if user_feed.div.div.text.lower() == port.lower():
					mini_soup = user_feed.find_all('div',class_='review-text')

					if verbose:
						print user_feed.div.div.text.strip()
						print user_feed.div.div.findNext().findNext().get('class', [])[2][-2].strip() + "/5 rating"
						print mini_soup[0].text.strip()

					f.write(user_feed.div.div.text.encode('utf-8').strip() + '\n')
					f.write(user_feed.div.div.findNext().findNext().get('class', [])[2][-2].encode('utf-8').strip() + "/5 rating" + '\n')
					f.write(mini_soup[0].text.encode('utf-8').strip().replace('\r', '').replace('\n', '') + '\n\n')

			user += 1

			if verbose:
				print "===========================\n"

		page_cnt += 1

		url = "https://www.cruisecritic.com/memberreviews/ports/" + port + "-cruises/" + "?page=" + str(page_cnt)
	else:
		break;

f.close()

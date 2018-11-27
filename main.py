#!/usr/bin/python

import html
from lxml import etree
import xml.etree.ElementTree as ET

import urllib2
#import urllib.request
from bs4 import BeautifulSoup

import csv

port = "shanghai"
#port = "beijing"

url = "https://www.cruisecritic.com/memberreviews/ports/" + port + "-cruises/"

user = 1

page_cnt = 1

#BUG
page_limit = 2

#b = open(port + '_feedbacks.csv', 'w')
#a = csv.writer(b)

f = open(port + '_feedbacks.csv', 'w')

while True:

	page = urllib2.urlopen(url)

	if( ( page.getcode() == 200 ) and (page_cnt < page_limit) ):

		soup = BeautifulSoup(page, "lxml")

		#######################################
		# print soup.prettify()
		# print soup.find_all("pb-3 review__description").prettify().encode(soup.original_encoding)

		# text = soup.prettify().encode(soup.original_encoding)
		# print text
		#######################################


		#######################################
		#feedbacks = soup.find_all('div', class_="pb-3 review__description")
		#
		#for feed in feedbacks:
		#    print feed.find_all('a',class_="chevron-after")
		#
		#print "\n\n"
		#######################################

		feedbacks = soup.find_all('a', class_="chevron-after")

		#user = 1

		for feed in feedbacks:
			# print feed.get("href")
			user_link = "https://www.cruisecritic.com" + feed.get("href")
		    
			# TMP
			#user_link = "https://www.cruisecritic.com/memberreviews/memberreview.cfm?EntryID=577854"

			#    print user_link
		    
			user_page = urllib2.urlopen(user_link).read()

			user_soup = BeautifulSoup(user_page, "lxml")

			user_details = user_soup.find_all('div',class_='review-author-details')

			user_date = user_soup.find_all('div',class_='heading__heavy--sm')

			print "==========================="
			print "User " + str(user) + " review:"
			print "==========================="

			#print user_details[0].span.text
			#print user_details[0].div.div.text

			#print user_details[0].span.next
			#print user_details[0].div.next.next.next
			#print user_details[0].div.div.next.next

			#print user_details[0]
			print user_details[0].span.text.strip()
			print user_details[0].div.div.text.strip()
			print user_details[0].div.div.findNext().div.text.strip()
			print user_date[0].findNext().li.text.strip()
			print user_details[0].div.div.findNext().div.findNext().text.strip()
			#    print user_details[0].div.div.findNext().div.findNext().findNext().findNext().text.split('\n', 1)[0]

			f.write(user_details[0].span.text.encode('utf-8').strip() + '\n')
			f.write(user_details[0].div.div.text.encode('utf-8').strip() + '\n')
			f.write(user_details[0].div.div.findNext().div.text.encode('utf-8').strip() + '\n')
			f.write(user_date[0].findNext().li.text.encode('utf-8').strip() + '\n')
			f.write(user_details[0].div.div.findNext().div.findNext().text.encode('utf-8').strip() + '\n')

			user_feedbacks = user_soup.find_all('li',class_='member-review__port-list-item')

			#    print user_feedbacks[1].div.div.text
			#mini_soup = user_feedbacks[1].find_all('div',class_='review-text')
			#print mini_soup[0].text
		   
			for user_feed in user_feedbacks:
				if user_feed.div.div.text.lower() == port.lower():
					# Use this print to see the Port
					print user_feed.div.div.text.strip()
					# print user_feed.div.div.findNext().findNext().get('class', [])[2]
					print user_feed.div.div.findNext().findNext().get('class', [])[2][-2].strip() + "/5 rating"
					mini_soup = user_feed.find_all('div',class_='review-text')
					print mini_soup[0].text.strip()

					f.write(user_feed.div.div.text.encode('utf-8').strip() + '\n')
					f.write(user_feed.div.div.findNext().findNext().get('class', [])[2][-2].encode('utf-8').strip() + "/5 rating" + '\n')
					f.write(mini_soup[0].text.encode('utf-8').strip() + '\n\n')

			#print user_feed.prettify()
		    
			user += 1
			#print "\n\n"

			print "===========================\n"

			#a.writerows(" ")

			#break

		page_cnt += 1

		url = "https://www.cruisecritic.com/memberreviews/ports/" + port + "-cruises/" + "?page=" + str(page_cnt)
	else:
		break;

# b.close()
f.close()

# encoding: utf-8
import random
import time
from selenium import webdriver

class Connection(object):
	def __init__(self):
		super(Connection, self).__init__()
		self.following = []

	def getstr(self):
		result = "{\n    \"following_ID\": \n    [\n"
		if len(self.following) == 0:
			result = result + "    \n    ]\n}"
			return result
		for fol in list(self.following)[:-1]:
			result = result + "        \"" + str(fol) + '\",\n'
		result = result + "        \"" + str(list(self.following)[-1]) + "\"\n    ]\n}"
		return result

def get_following(ID, driver):
	url = "https://medium.com/@" + str(ID)
	driver.get(url)
	time.sleep(3)
	connection = Connection()
	flag = 0
	button_list = driver.find_elements_by_class_name("button")
	for button in button_list:
		if button.get_attribute("data-action-value") == "following":
			button.click()
			time.sleep(2)
			flag = 1
			break
	if flag == 0:
		return connection
	size=0
	cnt=0
	cnt2=0
	while True:
		cnt2 = cnt2 + 1
		if cnt2 % 10 == 0:
			cnt = 0
		flag = 0
		button_list = driver.find_elements_by_class_name("button")
		for button in button_list:
			if button.get_attribute("data-action") == "load-more-follows":
				try:
					button.click()
				except:
					break
				time.sleep(2)
				flag = 1
				break
		if flag == 0:
			cnt = cnt + 1
			if cnt > 5:
				break
		following_list = driver.find_elements_by_class_name("link")
		if(len(following_list) > size):
			size = len(following_list)
		else:
			cnt = cnt + 1
			if cnt > 5:
				break
	print (len(following_list))
	cnt = 0
	for fol in following_list:
		if fol.get_attribute("data-action") == "show-user-card":
			cnt = cnt + 1
			if cnt % 2 == 1:
				if str(fol.get_attribute("href"))[20:] != str(ID):
					connection.following = connection.following + [str(fol.get_attribute("href"))[20:]]
	connection.following = set(connection.following)
	return connection
	

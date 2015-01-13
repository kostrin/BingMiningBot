from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class BingRewards(object):
    def __init__(self):
        self.rewardspage="https://www.bing.com/rewards/dashboard"
   
    #Only works on PC browser
    def printCurrentRewards(self, browser):
    	browser.get(self.rewardspage)
    	time.sleep(5)
        credits = browser.find_elements_by_class_name('credits')
        print "Current Credits: {}".format(credits[0].get_attribute("title"))
        print "Total Credits: {}".format(credits[1].get_attribute("title"))
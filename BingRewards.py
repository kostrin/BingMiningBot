from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class BingRewards(object):
    def __init__(self):
        self.rewardspage="https://www.bing.com/rewards/dashboard"
        self.pcTitle='pc search'
        self.mobileTitle = 'mobile search'
        self.notExtraTitles=[self.pcTitle, self.mobileTitle, 'invite friends']
   
    #Only works on PC browser
    def printCurrentRewards(self, browser):
        try:
            browser.get(self.rewardspage)
            time.sleep(1)
            credits = browser.find_elements_by_class_name('credits')
            print "  Current Credits: {}".format(credits[0].get_attribute("title"))
            print "  Total Credits: {}".format(credits[1].get_attribute("title"))
        except:
            print "Bing Service Error: Rewards couldn't be printed"

    def getRewardCounts(self, totalPCCount, totalMobileCount, browser):
        browser.get(self.rewardspage)
        time.sleep(1)
        elements=list(reversed(browser.find_elements_by_class_name('title')))
        titles=[item.text.lower() for item in elements]
        mobileIndex=titles.index(self.mobileTitle)
        pcIndex=titles.index(self.pcTitle)

        progress =  list(reversed(browser.find_elements_by_class_name('progress')))
        mobileCount= int(progress[mobileIndex].text.split()[0])
        pcCount = int(progress[pcIndex].text.split()[0])

        #print "{}-{}   {}-{}".format(totalPCCount,pcCount,totalMobileCount,mobileCount)
        return (totalPCCount-pcCount)*2, (totalMobileCount-mobileCount)*2

    def getExtraRewards(self, browser):
        browser.get(self.rewardspage)
        mainWindow = browser.current_window_handle
        time.sleep(2)

        try:
            element = browser.find_element_by_class_name('offers')
            for aTag in element.find_elements_by_tag_name('a'):
                if aTag.find_element_by_class_name('title').text.lower() not in self.notExtraTitles:
                    print "     Reward: {}".format(aTag.find_element_by_class_name('title').text.encode('cp850', errors='replace'))
                    aTag.click()

            #close unnecessary windows  
            for window in browser.window_handles:
                if window != mainWindow:
                    browser.switch_to_window(window)
                    browser.close()

            browser.switch_to_window(mainWindow)
        except:
            #catches the state change error when links are clicked
            pass
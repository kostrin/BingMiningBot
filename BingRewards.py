import os, sys,time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class BingRewards(object):
    def __init__(self, creds, rewardsHistory):
        self.rewardsPage="https://www.bing.com/rewards/dashboard"
        self.pcTitle='pc search'
        self.mobileTitle = 'mobile search'
        self.notExtraTitles=[self.pcTitle, self.mobileTitle, 'invite friends']
        
        #Target Reward
        self.redeemPage="https://www.bing.com/rewards/redeem"
        self.targetRewardMin=475
        self.targetRewardName="$5 Amazon.com Gift Card"
        self.targetRewardLabel="Amazon"
        self.minRewardTime=5
        self.credsCount=len(creds)
        self.rewardsHistoryFile=rewardsHistory

    #Only works on PC browser
    def getCurrentRewards(self, browser):
        try:
            browser.get(self.rewardsPage)
            time.sleep(1)
            credits = browser.find_elements_by_class_name('credits')
            return int(credits[0].get_attribute("title")), int(credits[1].get_attribute("title"))
        except:
            return 0,0

    def printCurrentRewards(self, browser):
        currentCredits, totalCredits = self.getCurrentRewards(self,browser)
        if(currentCredits>0 and totalCredits>0):
            print "  Current Credits: {}".format(currentCredits)
            print "  Total Credits: {}".format(totalCredits)
        else:
            print "Bing Service Error: Rewards couldn't be printed!"

    def getRewardCounts(self, totalPCCount, totalMobileCount, browser):
        browser.get(self.rewardsPage)
        time.sleep(1)
        groups=list(browser.find_elements_by_class_name('tileset'))
        elements=list(groups[1].find_elements_by_class_name('title'))
        titles=[item.text.lower() for item in elements]
        try:
            mobileIndex=titles.index(self.mobileTitle)
            pcIndex=titles.index(self.pcTitle)
            #print "mobile {}, pc {}".format(mobileIndex, pcIndex)

            groups=list(browser.find_elements_by_class_name('tileset'))
            progress =  list(groups[1].find_elements_by_class_name('progress'))
            mobileCount= int(progress[mobileIndex].text.split()[0])
            pcCount = int(progress[pcIndex].text.split()[0])

            #print "{}-{}   {}-{}".format(totalPCCount,pcCount,totalMobileCount,mobileCount)
            return (totalPCCount-pcCount)*2, (totalMobileCount-mobileCount)*2
        
        except:
            print "     Error: Rewards Page couldn't be displayed properly"
            return 0,0

    def getExtraRewards(self, browser):
        browser.get(self.rewardsPage)
        mainWindow = browser.current_window_handle
        time.sleep(2)

        try:
            element = browser.find_element_by_class_name('offers')
            for aTag in element.find_elements_by_tag_name('a'):
                if aTag.find_element_by_class_name('title').text.lower() not in self.notExtraTitles:
                    print "     Reward: {}".format(aTag.find_element_by_class_name('title').text.encode('cp850', errors='replace'))
                    aTag.click()
        except:
            #catches the state change error when links are clicked
            pass

        #close unnecessary windows
        time.sleep(2)
        for window in browser.window_handles:
            if window != mainWindow:
                browser.switch_to_window(window)
                browser.close()

        browser.switch_to_window(mainWindow)

    def cashInRewards(self, browser, user):
        if self.canCashInRewards(browser, user):
            print "Cashing in Reward for: {}".format(user)
            self.claimReward(browser, user)
            return True
        else:
            return False

    #TODO: Finish and TEST!
    def claimReward(self, browser, user):
        browser.get(self.redeemPage)
        rewardPage=""
        time.sleep(1)
        for aTag in browser.find_elements_by_tag_name('a'):
            for nameTag in aTag.find_elements_by_class_name('name'):
                if nameTag.text.lower() == self.targetRewardName.lower():
                    rewardPage=aTag.get_attribute("href")
                    break

        browser.get(rewardPage)
        time.sleep(5)
        #finish clicking, hope that close will close all
        
        time.sleep(5)
        with open(self.rewardsHistoryFile, 'ab+') as f:
            f.write('{} {} {}\n'.format( datetime.now().strftime("%m/%d"),user,self.targetRewardLabel))

    #TODO: TEST!
    def canCashInRewards(self,browser, user):
        currentCredits, totalCredits = self.getCurrentRewards(browser)
        lastDate, lastAccounts = self.getCashedHistory()
        #(currentCredits>=self.targetRewardMin) and 
        if ((user not in lastAccounts) and
            (lastDate==None or datetime.now()>= lastDate + timedelta(days=self.minRewardTime))):

            return True
        else:
            return False

    def getCashedHistory(self):
        neededAccounts = self.credsCount-1
        if self.isUnemptyFile(self.rewardsHistoryFile):
            try:
                #Get last time user cashed in
                lastEntry=list(open(self.rewardsHistoryFile))[-1]
                lastDate=datetime.strptime(lastEntry.split()[0], "%m/%d")
                lastAccounts=[]

                #Get Last n-1 accounts cashed in
                for line in reversed(list(open(self.rewardsHistoryFile))):
                    
                    lastAccounts.append(line.split()[1])
                    neededAccounts-=1
                    if neededAccounts<=0:
                        break
                return lastDate, lastAccounts
            except:
                print "File Error: Error reading rewards history."
                sys.exit()
        else:
           return None, []

    def isUnemptyFile(self,fpath):  
        return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False
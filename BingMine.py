import argparse
import time
from random import randint

from BingAuth import BingAuth
from BingRewards import BingRewards
from BingRequests import BingRequests

#cron
#python BingMine.py | exit

class BingMine(object):

    def __init__(self,mobileAttempts=30,pcAttempts=46, upperWait=5, lowerWait=3):
        self.mobileAttempts=pcAttempts
        self.pcAttempts=mobileAttempts
        self.upperWait=upperWait
        self.lowerWait=lowerWait

        self.bingAuth = BingAuth()
        self.bingRewards = BingRewards()
        self.bingRequests = BingRequests()
        
    def parseArgs(self):
        parser = argparse.ArgumentParser(prog='Mine Bing Rewards', description='Will mine your Bing rewards for the day.', add_help=True)
        parser.add_argument('-c', '--credsFile', type=str, help='credentials to mine', default='credentials.txt')
        args = parser.parse_args()
        self.creds=self.getCreds(args.credsFile)

    def getRewards(self):
        if not self.creds:
            print "No valid credentials!"
            return

        print time.strftime("%c")

        for accountList in self.creds:
            user=accountList[0]
            passwd=accountList[1]
            accType=accountList[2]
            self.browser=None
            print 'Running on account: %s'% (user)
            
            userAgent=self.bingRequests.getMobileUserAgent()
            browser=self.bingAuth.login(user, passwd, userAgent, accType.lower())
            self.makeAllRequests(self.mobileAttempts, browser)
            browser.quit()
            
            userAgent=self.bingRequests.getPCUserAgent()
            browser=self.bingAuth.login(user, passwd, userAgent, accType.lower())
            self.makeAllRequests(self.pcAttempts, browser)
            self.bingRewards.printCurrentRewards(browser)
            browser.quit()
 
        #TODO: clear history   
            
            
    def makeAllRequests(self, attempts, browser):
        inc=0
        while(inc<attempts):
            self.bingRequests.makeRequest(browser)
            time.sleep(randint(self.lowerWait,self.upperWait))
            inc+=1 
            
    def getCreds(self, credsFile):
        #USAGE: USER PASS Type
        #NOTE: 1 user per line
        creds=[]
        with open(credsFile) as f:
            credsX=[]
            for line in f:
                if line[0]=='#':
                    pass
                else:
                    data=line.split()
                    creds.append(data)
        return creds

if __name__ == "__main__":
    b = BingMine()
    b.parseArgs()
    b.getRewards()

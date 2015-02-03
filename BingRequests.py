from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from faker import Faker
from random import randint
import urllib

class BingRequests(object):
    def __init__(self):
        self.baseSearchURL="http://www.bing.com/search?q="
        self.useragentPC = [
            # Safari 7.0 MacOSX
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/7.0.1 Safari/537.73.11",
            # Chrome 31.0 Win7 64-bit
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
            # Firefox 26.0 Win7 64-bit
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0",
            # Chrome 32.0 Win7 64-bit
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36",
            # Chrome 31.0 MacOSX
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
            # Chrome 32.0 MacOSX
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36",
            # Firefox 26.0 MacOSX
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:26.0) Gecko/20100101 Firefox/26.0",
            # Chrome 31.0 Win8.1 64-bit
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
        ]
        self.useragentMobile = [
                # Android 4.0.2
                    "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
                # Android 2.3
                    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                # BlackBerry - BB10
                    "Mozilla/5.0 (BB10; Touch) AppleWebKit/537.1+ (KHTML, like Gecko) Version/10.0.0.1337 Mobile Safari/537.1+",
                # iPhone - iOS 7
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A4449d Safari/9537.53",
                # iPhone - iOS 6
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
                # iPhone - iOS 9
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.12 (KHTML, like Gecko) Version/8.0 Mobile/13A150 Safari/600.1.4",
                # iPhone - iOS 8
                    "Mozilla/5.0 (iPad; CPU OS 8_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/8.0 Mobile/11A465 Safari/9537.53"
        ]

    def makeRequest(self, browser):
        query=self.generateQuery()
        browser.get(self.baseSearchURL+urllib.quote(query))

    def getMobileUserAgent(self):
        return self.useragentMobile[randint(0,6)]
    
    def getPCUserAgent(self):
        return self.useragentPC[randint(0,7)]

    def generateQuery(self):
        faker=Faker()
        number = randint(0,6)
        if number == 0:
            string = faker.full_address()
        elif number == 1:
            string = faker.name()
        elif number == 2:
            string = faker.username()
        elif number == 3:
            string = faker.email()
        elif number == 4:
            string = faker.city()
        else:
            string = faker.company()
        return string.decode('utf8')
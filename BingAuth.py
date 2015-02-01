from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from BingRequests import BingRequests

class BingAuth(object):
    def __init__(self):
        self.bingAuth=BingRequests()
        self.liveLoginPage = "https://www.bing.com/fd/auth/signin?action=interactive&provider=windows_live_id&return_url=https%3a%2f%2fwww.bing.com%2f"
        self.liveLogoffPage = ""
        self.facebookLoginPage = ""
        self.facebookLogoffPage = ""

    def createBrowser(self, userAgent):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override",userAgent)
        browser=webdriver.Firefox(profile)
        browser.set_window_size(300,300)
        browser.set_window_position(-300,-300)
        return browser

    def login(self, username, passwd, userAgent, accType):
        browser=self.createBrowser(userAgent)
        if accType == 'facebook':
            self.facebookLogin(browser, username, passwd)
        else:
            self.liveLogin(browser, username, passwd)
        return browser

    def liveLogin(self, browser, username, passwd):
        browser.get(self.liveLoginPage)
        emailField = browser.find_element_by_name('login')
        emailField.send_keys(username)
        passwordField = browser.find_element_by_name('passwd')
        passwordField.send_keys(passwd)
        browser.find_element_by_name('KMSI').click()
        passwordField.submit()
        time.sleep(3)
    
    #TODO
    def liveLogout(self):
        pass
    def facebookLogin(self, browser, username, passwd):
        pass
    def facebookLogout(self):
        pass
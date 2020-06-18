from selenium import webdriver
import logging
import time
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from retrying import retry
from selenium.webdriver import ActionChains

import pyautogui
pyautogui.PAUSE = 0.5 

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class taobao():
    def __init__(self):
        self.browser = webdriver.Chrome("path\to\your\chromedriver.exe")
        self.browser.maximize_window()
        self.browser.implicitly_wait(5)
        self.domain = 'http://www.taobao.com'
        self.action_chains = ActionChains(self.browser)

    def login(self, username, password):
        while True:
            self.browser.get(self.domain)
            time.sleep(1)

            #self.browser.find_element_by_class_name('h').click()
            #self.browser.find_element_by_id('fm-login-id').send_keys(username)
            #self.browser.find_element_by_id('fm-login-password').send_keys(password)
            self.browser.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]').click()
            self.browser.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
            self.browser.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password)
            time.sleep(1)

            try:
                # using Selenium ActionChains for the website SLIDE authentication
                slider = self.browser.find_element_by_xpath("//span[contains(@class, 'btn_slide')]")
                if slider.is_displayed():
                    # pull the slider
                    self.action_chains.drag_and_drop_by_offset(slider, 258, 0).perform()
                    time.sleep(0.5)
                    # release the slider
                    self.action_chains.release().perform()
            except (NoSuchElementException, WebDriverException):
                logger.info('slider not found')

            # using pyautogui click the LOGIN PNG image
            #self.browser.find_element_by_class_name('password-login').click()
            #self.browser.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
             coords = pyautogui.locateOnScreen('1.png')
            x, y = pyautogui.center(coords)
            pyautogui.leftClick(x, y)

            nickname = self.get_nickname()
            if nickname:
                logger.info('successfully logon, nickname is' + nickname)
                break
            logger.debug('login failed，please try again after 5 seconds')
            time.sleep(5)

    def get_nickname(self):
        self.browser.get(self.domain)
        time.sleep(0.5)
        try:
            return self.browser.find_element_by_class_name('site-nav-user').text
        except NoSuchElementException:
            return ''


if __name__ == '__main__':
    # Input your TAOBAO username and password
    username = 'username'
    password = 'password'
    tb = taobao()
    tb.login(username, password)

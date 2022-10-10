import selenium as sl
from selenium import webdriver
from time import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('disable-notifications')

browser = webdriver.Chrome('chromedriver.exe', options=chrome_options)
browser.maximize_window()

browser.get('https://www.trendyol.com/sr?q=air force')
delay = 3
try:    
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located(("xpath", "//*[@id='onetrust-accept-btn-handler']")))
    print("Cookies Accepted")

    # Click on the cookies button
    browser.find_element("xpath", "//*[@id='onetrust-accept-btn-handler']").click()

    # Click on the page once
    browser.find_element("xpath", '//*[@id="search-app"]/div/div[1]/div[2]/div[4]/div[1]/div/div[2]/div[1]/a/div[2]').click() #

except:
    print("Loading took too much time!")
    browser.quit()

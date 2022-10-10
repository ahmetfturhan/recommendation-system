import selenium as sl
from selenium import webdriver
from time import *


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('disable-notifications')

browser = webdriver.Chrome('chromedriver.exe', options=chrome_options)
browser.maximize_window()

browser.get('https://www.trendyol.com/sr?q=air force')
sleep(1)
browser.find_element("xpath", "//*[@id='onetrust-accept-btn-handler']").click()
sleep(1)
browser.find_element("xpath", '//*[@id="search-app"]/div/div[1]/div[2]/div[4]/div[1]/div/div[2]/div[1]/a/div[2]').click()

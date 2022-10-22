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

search_query = "air force"
brand = "Nike"

browser.get('https://www.trendyol.com/sr?q=' + search_query)
delay = 3
 
myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located(("xpath", "//*[@id='onetrust-accept-btn-handler']")))
print("Cookies Accepted")

# Click on the cookies button
browser.find_element("xpath", "//*[@id='onetrust-accept-btn-handler']").click()

# Click on the page once
browser.find_element("xpath", '/html/body/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div[4]/div[1]/a/div[2]').click() #

# Find the brand filters
trend_brand_filters = browser.find_element(By.CSS_SELECTOR, 'div[data-title="Marka"]')

# Find the parent of the brand filters to access the children
trend_brand_filters_parent = trend_brand_filters.get_property('parentElement')

# Find the list of brands
trend_brand_filters_name_list = trend_brand_filters_parent.find_element(By.CLASS_NAME, 'fltrs').get_property('children')

# Find the requested brand and click on it
for i in trend_brand_filters_name_list:
    if i.text == brand:
        i.click()
        break



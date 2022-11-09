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
delay = 5
 
myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located(("xpath", "//*[@id='onetrust-accept-btn-handler']")))
print("Cookies Accepted")

# Click on the cookies button
browser.find_element("xpath", "//*[@id='onetrust-accept-btn-handler']").click()

# Click on the page once
browser.find_element("xpath", '//*[@id="search-app"]/div/div[1]/div[2]/div[4]/div[1]/div/div[3]/div[1]/a/div[2]').click() #

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

sleep(5)

trend_product_card = browser.find_element(By.XPATH, '//*[@id="search-app"]/div/div[1]/div[2]/div[5]/div[1]/div/div[2]').find_element(By.CLASS_NAME, 'p-card-chldrn-cntnr')

trend_product_card_class = trend_product_card.find_element(By.CLASS_NAME, 'product-down')

trend_product_desc = trend_product_card_class.get_property('children')[0].find_element(By.CLASS_NAME, 'prdct-desc-cntnr').find_element(By.CLASS_NAME, 'prdct-desc-cntnr-ttl-w').find_element(By.CLASS_NAME, 'prdct-desc-cntnr-name').text
print(trend_product_desc)

trend_rating_count = trend_product_card_class.find_element(By.CLASS_NAME, 'ratings-container').find_element(By.CLASS_NAME, 'ratings').find_element(By.CLASS_NAME, 'ratingCount').text
print(trend_rating_count)

# If a product has a discounted price, the container name changes, so covering that case.
try: 
    trend_price = trend_product_card_class.find_element(By.CLASS_NAME, 'price-promotion-container').find_element(By.CLASS_NAME, 'prc-cntnr').find_element(By.CLASS_NAME, 'prc-box-dscntd').text
    print(trend_price)
except:
    trend_price = trend_product_card_class.find_element(By.CLASS_NAME, 'price-promotion-container').find_element(By.CLASS_NAME, 'prmtn-cntnr').find_element(By.CLASS_NAME, 'prc-box-dscntd').text
    print(trend_price)


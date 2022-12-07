import sys
import selenium as sl
import multiprocessing as mp
from selenium import webdriver
from time import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import StaleElementReferenceException
from faker import Faker
from selenium.webdriver.chrome.service import Service
import time
import json

class Product:
    def __init__(self, name, price, link, image, rating, rating_count, merchant):
        self.name = name
        self.price = price
        self.link = link
        self.image = image
        self.rating = rating
        self.rating_count = rating_count
        self.merchant = merchant


class Merchant:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating


def print_product(product):
    print("Name:", product.name)
    print("Price:", product.price)
    print("Link:", product.link)
    print("Image:", product.image)
    print("Rating:", product.rating)
    print("Rating Count:", product.rating_count)
    print("Merchant:", product.merchant.name)
    print("Merchant Rating:", product.merchant.rating)
    print("")

def check_exists_by_class(class_name, browser):
    try:
        browser.find_element(By.CLASS_NAME, class_name)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_css(css_selector, browser):
    try:
        browser.find_element(By.CSS_SELECTOR, css_selector)
    except NoSuchElementException:
        return False
    return True
    
def remove_items(test_list, item):
 
    # using list comprehension to perform the task
    res = [i for i in test_list if i != item]
 
    return res

def trendyol(trend_product_list, brand, search_query):
    print("Starting Trendyol")
    start = time.time()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome('chromedriver.exe', options=chrome_options)
    browser.maximize_window()
    
    browser.get('https://www.trendyol.com/sr?q=' + search_query)
    delay = 5

    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located(("xpath", "//*[@id='onetrust-accept-btn-handler']")))
    print("Cookies Accepted")

    # Click on the cookies button
    browser.find_element("xpath", "//*[@id='onetrust-accept-btn-handler']").click()

    # Click on the page once
    if check_exists_by_class('overlay', browser):
        browser.find_element(By.CLASS_NAME, 'overlay').click() #
                                                            
    if brand != "default":
        # Find the brand filters
        trend_brand_filters = browser.find_element(By.CSS_SELECTOR, 'div[data-title="Marka"]')

        # Find the parent of the brand filters to access the children
        trend_brand_filters_parent = trend_brand_filters.get_property('parentElement')

        # Find the list of brands
        trend_brand_filters_name_list = trend_brand_filters_parent.find_element(By.CLASS_NAME, 'fltrs').get_property('children')

        # Find the requested brand and click on it
        for i in trend_brand_filters_name_list:

            if i.text.lower() == brand.lower():
                i.click()
                break

    browser.implicitly_wait(5)
    trend_products_div = WebDriverWait(browser,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "p-card-wrppr")]')))

    print("Total found products: ", len(trend_products_div))
 
    trend_link_list = []
    trend_product_list = []

    for i, item in enumerate(trend_products_div):
        if i == 10:
            break
        print("Loading",(i / len(trend_products_div))*100,"%")

        # get product descriptions
        try:
            trend_product_desc = item.find_element(By.XPATH, './/span[contains(@class, "prdct-desc-cntnr-name")]').text
            # print(trend_product_desc)

        except StaleElementReferenceException as e:
            trend_product_desc = "0"
            print("StaleElementReferenceException")
        
        # get ratings
        try:
            trend_product_rating_count = item.find_element(By.XPATH, './/span[contains(@class, "ratingCount")]').text
            trend_product_rating_count = trend_product_rating_count.replace("(", "")
            trend_product_rating_count = trend_product_rating_count.replace(")", "")
    
        except Exception as e:
            print("Couldn't get rating", e)
            trend_product_rating_count = "0"            
        
        # get prices
        try:
            trend_product_price_box = item.find_element(By.XPATH, './/div[contains(@class, "price-promotion-container")]')
            trend_product_price = trend_product_price_box.find_element(By.XPATH, './/div[contains(@class, "prc-box-dscntd")]').text
        except Exception as e:
            trend_product_price = "0"
            print("Couldn't get price", e)

        # get links
        try:
            trend_product_link = item.find_element(By.XPATH, './/div[contains(@class, "p-card-chldrn-cntnr")]/a').get_property('href')
            trend_link_list.append(trend_product_link)
        except Exception as e:
            trend_product_link = "0"
            trend_link_list.append(trend_product_link)
            print("Couldn't get link", e)
        
                #create a product object
        new_product = Product(trend_product_desc, trend_product_price, trend_product_link, "0", 0 ,trend_product_rating_count, Merchant("null", "null"))
        trend_product_list.append(new_product)

    # product pages        
    for j, link in enumerate(trend_link_list):
        if j == 10:
            break
        browser.get(link)

        #wait for max 10 seconds to load the page
        WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product-seller-line"))
    )
        # get images
        try:
            #get img link
            trend_product_img = browser.find_element(By.XPATH, '//div[contains(@class, "base-product-image")]/div/img').get_property('src')
        except Exception as e:
            trend_product_img = "09"
            print("Couldn't get img", e)
        
        #get merchant
        try:
            trend_product_merchant_name = browser.find_element(By.XPATH, '//div[contains(@class, "seller-container")]/a').text
            trend_product_merchant_rating_box = browser.find_element(By.XPATH, '//div[contains(@class, "product-seller-line")]')
        except Exception as e:
            trend_product_merchant_name = "0"
            print("Couldn't get merchant name", e)

        try:    
            trend_product_merchant_rating = trend_product_merchant_rating_box.find_element(By.XPATH, './/div[contains(@class, "sl-pn")]').text
        except Exception as e:
            trend_product_merchant_rating = "0"
            print("Couldn't get merchant", e)

        #create a merchant object
        new_merchant = Merchant(trend_product_merchant_name, trend_product_merchant_rating)
        trend_product_list[j].merchant = new_merchant
        trend_product_list[j].image = trend_product_img

    # print("Trendyol Products:\n")
    # for i in trend_product_list:
    #     print_product(i)
    
    browser.quit()    
    end = time.time()
    print("The time of execution of Trendyol script is :",
      (end-start) * 10**3, "ms")
    trendyol_matched_products = []

    # for item in desc_list:
    #     if search_query.lower() in item.lower() and "kulaklık" not in item.lower() and "kılıf" not in item.lower():
    #         trendyol_matched_products.append(item)
    # return trendyol_matched_products

    

def amazon(amazon_product_list_main, brand, search_query):
    print("Starting Amazon")
    start = time.time()
    # random user agent generator
    # fake = Faker()
    # random_ua = fake.user_agent()
    # print("fake user agent: ", random_ua)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('disable-notifications')

    #random user agent
    # chrome_options.add_argument(f'user-agent="{random_ua}"')

    chrome_options.add_argument('--headless')

    service_obj = Service(rf"C:\Users\ahmet\AppData\Local\Programs\Python\Python39\chromedriver.exe")

    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])


    browser = webdriver.Chrome('chromedriver.exe', options=chrome_options, service=service_obj)
    browser.maximize_window()



    browser.get('https://www.amazon.com.tr/s?k=' + search_query)
    delay = 5

    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located(("xpath", '//*[@id="sp-cc-accept"]')))
    print("Cookies Accepted")

    # Click on the cookies button
    browser.find_element("xpath", '//*[@id="sp-cc-accept"]').click()

    browser.implicitly_wait(2)

    amazon_brand_filters = browser.find_element(By.ID, 'brandsRefinements').find_element(By.CLASS_NAME, 'a-unordered-list').get_property('children')
    
    #Select the brand
    for i in amazon_brand_filters:
        brand_name = i.find_element(By.CLASS_NAME, 'a-list-item').find_element(By.CLASS_NAME, 'a-link-normal').find_element(By.CLASS_NAME, 'a-size-base').text
        print("brands", brand_name)
        if i.text.lower() == brand.lower():
            i.find_element(By.CLASS_NAME, 'a-list-item').find_element(By.CLASS_NAME, 'a-link-normal').click()
            break
    
    # browser.implicitly_wait(3)


    product_desc = []
    product_asin = []
    product_price = []
    product_ratings = []
    product_ratings_num = []
    product_link = []
    product_merchant = []

    amazon_product_list = []
    amazon_merchant_list = []
    items = WebDriverWait(browser,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
    for j, item in enumerate(items):
        if j == 10:
            break
        #Get descriptions
        amazon_product_desc = item.find_element(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]')

        # Find price
        amazon_whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
        amazon_fraction_price = item.find_elements(By.XPATH,'.//span[@class="a-price-fraction"]')

        if amazon_whole_price != [] and amazon_fraction_price != []:
            price = '.'.join([amazon_whole_price[0].text, amazon_fraction_price[0].text])
        else:
            price = 0

        #get rratings
        amazon_rating_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

        if amazon_rating_box != []:
            amazon_ratings = amazon_rating_box[0].get_attribute('aria-label')
            amazon_rating_num = amazon_rating_box[1].get_attribute('aria-label')
        else:
            ratings = 0
            ratings_num = 0
        product_ratings.append(amazon_ratings)
        product_ratings_num.append(amazon_rating_num)

        #get links
        amazon_product_link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute('href')
        product_link.append(amazon_product_link)

        new_product = Product(amazon_product_desc.text, price, amazon_product_link, "09", amazon_ratings, amazon_rating_num, "000")
        amazon_product_list.append(new_product)

    for i, link in enumerate(product_link):
        if i == 10:
            break
        browser.get(link)
        # browser.implicitly_wait(3)
        WebDriverWait(browser,10).until(EC.presence_of_all_elements_located((By.XPATH, '//img[@id="landingImage"]')))

        #Get merchant info
        try:
            merchant_info = browser.find_elements(By.XPATH, './/div[@id="merchant-info"]/a')

            if len(merchant_info) != 0:
                merchant_name = merchant_info[0].text
                product_merchant.append(merchant_name)
            else:
                merchant_name = "Amazon.com.tr"   

        except:
            merchant_name = "Amazon.com.tr"   
        
        #Get image
        try:
            amazon_image = browser.find_element(By.XPATH, '//img[@id="landingImage"]')
            amazon_image_src = amazon_image.get_attribute('src')
        except:
            amazon_image_src = "0"
        
        new_merchant = Merchant(merchant_name, 0)
        amazon_merchant_list.append(new_merchant)

        # amazon_product_list[i].merchant = new_merchant
        # amazon_product_list[i].image = amazon_image_src

    for i, item in enumerate(amazon_product_list):
        product_obj = Product(item.name, item.price, item.link, item.image, item.rating, item.rating_count, amazon_merchant_list[i])
        amazon_product_list_main.append(product_obj)

    product_string = brand.lower() + " " + search_query.lower()

    # amazon_matched_products = []
    # for desc in product_desc:
    #     if product_string in desc.lower() and "kılıf" not in desc.lower():
    #         amazon_matched_products.append(desc)

    # print("Amazon Products:\n")
    # for i in amazon_product_list:
    #     print_product(i)

    browser.quit()
    end = time.time()
    print("The time of execution of Amazon script is :",
      (end-start) * 10**3, "ms")
    # return amazon_matched_products

    return amazon_product_list




if __name__ == '__main__':
    search_query = sys.argv[1]
    brand = sys.argv[2]
    
    manager = mp.Manager()
    trendyol_product_list_main = manager.list()
    amazon_product_list_main = manager.list()

    # trendyol_process = mp.Process(target=trendyol,args=(trendyol_product_list_main, brand,search_query))
    # trendyol_process.start()
    amazon_process = mp.Process(target=amazon, args=(amazon_product_list_main, brand,search_query))
    amazon_process.start()

    # trendyol_process.join()
    amazon_process.join()

    # print("Trendyol items\n", trendyol_product_list_main)
    # for i in trendyol_product_list_main:
    #     print_product(i)

    print("Amazon items\n\n\n", amazon_product_list_main)
    for i in amazon_product_list_main:
        print_product(i)

#trendyol_items = trendyol(browser, brand, search_query)
#amazon_items = amazon(browser, brand, search_query)
# print("Trendyol items\n", trendyol_items)
# print("Amazon items\n\n\n", amazon_items)
#browser.quit()
#exit(0)
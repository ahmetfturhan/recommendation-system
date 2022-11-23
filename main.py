import selenium as sl
from selenium import webdriver
from time import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException 

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

def trendyol(browser, brand, search_query):
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

    trend_products_div = browser.find_element(By.CLASS_NAME, 'prdct-cntnr-wrppr').get_property('children')
    desc_list = []
    for i in trend_products_div:
        try:
            trend_product_card = i.find_element(By.CLASS_NAME, 'p-card-chldrn-cntnr')

            trend_product_card_class = trend_product_card.find_element(By.CLASS_NAME, 'product-down')

            trend_product_desc = trend_product_card_class.get_property('children')[0].find_element(By.CLASS_NAME, 'prdct-desc-cntnr').find_element(By.CLASS_NAME, 'prdct-desc-cntnr-ttl-w').find_element(By.CLASS_NAME, 'prdct-desc-cntnr-name').text
            desc_list.append(trend_product_desc)
            #print(desc_list)
            # print((trend_product_desc))
        except Exception as e:
            continue

        #Some products don't have ratings
        try:
            trend_rating_count_container = trend_product_card_class.find_element(By.CLASS_NAME, 'ratings-container')
            trend_ratings = trend_rating_count_container.find_element(By.CLASS_NAME, 'ratings')
            trend_rating_count = trend_ratings.find_element(By.CLASS_NAME, 'ratingCount').text
            # print(trend_rating_count)
        except Exception as e:
            print("Cannot find rating", e)

        try:
            # If a product has a discounted price, the container name changes, so covering that case.
            if check_exists_by_class('price-promotion-container', browser):
                try: 
                    #Düz fiyat ve çizgili fiyat caseleri
                    trend_price = trend_product_card_class.find_element(By.CLASS_NAME, 'price-promotion-container').find_element(By.CLASS_NAME, 'prc-cntnr').find_element(By.CLASS_NAME, 'prc-box-dscntd').text 
                    # print(trend_price)

                except Exception as e:
                    #Sepet fiyatı case
                    trend_price = trend_product_card_class.find_element(By.CLASS_NAME, 'price-promotion-container').find_element(By.CLASS_NAME, 'prmtn-cntnr').get_property('children')[0].find_element(By.CLASS_NAME, 'prmtn').find_element(By.CLASS_NAME, 'prc-box-dscntd').text
                    # print(trend_price)
            
        except Exception as e:
            print("Cannot find price", e)
    print(desc_list)
    trendyol_matched_products = []
    for item in desc_list:
        if search_query.lower() in item.lower() and "kulaklık" not in item.lower() and "kılıf" not in item.lower():
            trendyol_matched_products.append(item)
    return trendyol_matched_products

def amazon(browser, brand, search_query):
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
    
    browser.implicitly_wait(3)


    product_desc = []
    product_asin = []
    product_price = []
    product_ratings = []
    product_ratings_num = []
    product_link = []
    product_merchant = []

    items = WebDriverWait(browser,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
    for item in items:
        
        #Get descriptions
        amazon_product_desc = item.find_element(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]')
        product_desc.append(amazon_product_desc.text)

        # Find price
        amazon_whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
        amazon_fraction_price = item.find_elements(By.XPATH,'.//span[@class="a-price-fraction"]')

        if amazon_whole_price != [] and amazon_fraction_price != []:
            price = '.'.join([amazon_whole_price[0].text, amazon_fraction_price[0].text])
        else:
            price = 0
        product_price.append(price)

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

    # for link in product_link:
    #     browser.get(link)
    #     browser.implicitly_wait(3)
    #     merchant_info = browser.find_elements(By.XPATH, './/div[@id="merchant-info"]/span')
    #     merchant_name = merchant_info[0].text
    #     product_merchant.append(merchant_name)
        
    
    product_string = brand.lower() + " " + search_query.lower()
    amazon_matched_products = []
    for desc in product_desc:
        if product_string in desc.lower() and "kılıf" not in desc.lower():
            amazon_matched_products.append(desc)

    
    # print(product_price)
    # print(product_ratings)
    # print(product_ratings_num)
    # print(product_link)
    # print(product_merchant)
    browser.implicitly_wait(2)

    browser.quit()
    return amazon_matched_products

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--headless')
browser = webdriver.Chrome('chromedriver.exe', options=chrome_options)
browser.maximize_window()

search_query = "iphone 11"
brand = "apple"

trendyol_items = trendyol(browser, brand, search_query)
amazon_items = amazon(browser, brand, search_query)
print("Trendyol items\n", trendyol_items)
print("Amazon items\n\n\n", amazon_items)

matched_products = []
for t in trendyol_items:
    for a in amazon_items:
        t = t.lower()
        a = a.lower()
        t = t.replace('(', '')
        t = t.replace(')', '')
        t = t.replace('-', '')

        a = a.replace('(', '')
        a = a.replace(')', '')
        a = a.replace('-', '')

        trendyol_split = t.split(" ")
        amazon_split = a.split(" ")

        trendyol_split = remove_items(trendyol_split, "")
        amazon_split = remove_items(amazon_split, "")

        print("\nAmazon split, ", amazon_split)
        print("\nTrendyol split, ", trendyol_split)
        match_counter = 0
        if len(trendyol_split) > len(amazon_split):
            for i in amazon_split:
                for j in trendyol_split:
                    if i == j:
                        match_counter += 1
                        break

            if match_counter >= int(len(amazon_split)*0.90):
                print("Matched", t, a)
                matched_products.append([a, t])

        else:
            match_counter = 0
            for i in trendyol_split:
                for j in amazon_split:
                    if i == j:
                        match_counter += 1
                        break

            if match_counter >= int(len(trendyol_split)*0.90):
                print("Matched", t, a)
                matched_products.append([a, t])

print(matched_products)




import logging
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
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
import argparse
import string


class Product:
    def __init__(self, name, price, link, image, rating, rating_count, merchant_name, merchant_rating, website):
        self.name = name
        self.price = price
        self.link = link
        self.image = image
        self.rating = rating
        self.rating_count = rating_count
        self.merchant_name = merchant_name
        self.merchant_rating = merchant_rating
        self.formula_rank = 0
        self.website = website


class Merchant:
    def __init__(self, name, rating, image):
        self.name = name
        self.rating = rating
        self.image = image

def match_similar(trproduct, amproduct, similarity_rate):
    first = remove_punctuation(trproduct)
    second = remove_punctuation(amproduct)

    match_counter = 0
    if len(first) > len(second):
        for i in second:
            for j in first:
                if i == j:
                    match_counter += 1
                    break

        if match_counter >= int(len(second) * similarity_rate):
            # print("Matched", amproduct.name,"|||", trproduct.name)
            # return [amproduct, trproduct]
            return True
            
    else:
        match_counter = 0
        for i in first:
            for j in second:
                if i == j:
                    match_counter += 1
                    break

        if match_counter >= int(len(first) * similarity_rate):
            # print("Matched", amproduct.name,"|||", trproduct.name)
            # return [amproduct, trproduct]
            return True
    return False
    # return []

def match_exact(trproduct, amproduct):
    first = remove_punctuation(trproduct)
    second = remove_punctuation(amproduct)

    match_counter = 0
    if len(first) > len(second):
        for i in second:
            for j in first:
                if i == j:
                    match_counter += 1
                    break

        #Exact matching
        if match_counter == len(second):
            # print("Matched", amproduct.name,"|||", trproduct.name)
            # return [amproduct, trproduct]
            return True
            

    else:
        match_counter = 0
        for i in first:
            for j in second:
                if i == j:
                    match_counter += 1
                    break

        #Exact matching
        if match_counter == len(first):
            # print("Matched", amproduct.name,"|||", trproduct.name)
            # return [amproduct, trproduct]
            return True

    return False

def remove_punctuation(trproduct):
    t = trproduct.name

    t = t.lower()
    t = t.replace('|', '')
    t = t.translate(str.maketrans('', '', string.punctuation))


    split = t.split(" ")

    #Remove empty chars
    split = remove_items(split, "")
    return split

def print_product(product):
    logging.info("Name:", product.name)
    logging.info("Price:", product.price)
    logging.info("Link:", product.link)
    logging.info("Image:", product.image)
    logging.info("Rating:", product.rating)
    logging.info("Rating Count:", product.rating_count)
    logging.info("Merchant:", product.merchant.name)
    logging.info("Merchant Rating:", product.merchant.rating)
    logging.info("")

def check_exists_by_class(class_name, browser):
    try:
        browser.find_element(By.CLASS_NAME, class_name)
    except NoSuchElementException:
        return False
    return True

def remove_items(test_list, item):
 
    # using list comprehension to perform the task
    (res := [i for i in test_list if i != item])
 
    return res

def trendyol(trend_product_list_main, brand, search_query):
    product_number = 8
    print("Starting Trendyol")
    start = time.time()
    
# Print the ChromeDriver version
    

# Set the vhs options
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--enable-gpu')
    browser = webdriver.Chrome('chromedriver.exe', options=chrome_options)
    browser.maximize_window()
    
    browser.get('https://www.trendyol.com/sr?q=' + search_query)
    delay = 5

    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located(("xpath", "//*[@id='onetrust-accept-btn-handler']")))
    print("Trendyol Cookies Accepted")

    # Click on the cookies button
    browser.find_element("xpath", "//*[@id='onetrust-accept-btn-handler']").click()

    # Click on the page once
    if check_exists_by_class('overlay', browser):
        browser.find_element(By.CLASS_NAME, 'overlay').click() #
                                                            

    try:
        if brand != "default":
            trend_brand_filter = browser.find_element("xpath", '//div[@data-title="Marka"]')

            # Find siblings that come after the marka element
            trend_filters = trend_brand_filter.find_element("xpath", './following-sibling::*')
            
            brand_list = trend_filters.find_elements("xpath", './/div[@class="ReactVirtualized__Grid__innerScrollContainer"]/div')
            
            for i in brand_list:
                if i.text.lower() == brand.lower():
                    i.find_element("xpath", './/div[@class="chckbox"]').click()
                    break
            print("trendyol selected brand")
    except Exception as e:
        print("Couldn't select the brand", e)
    sleep(1)
    browser.refresh()
    trend_products_div = WebDriverWait(browser,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "p-card-wrppr")]')))

    logging.info("Total found products: %d", len(trend_products_div))
 
    trend_link_list = []
    trend_product_list = []
    trend_merchant_list = []
    trend_temp_list = []
    trend_rating_list = []

    for i, item in enumerate(trend_products_div):
        if i == product_number:
            break
        progress = (i / len(trend_products_div)) * 100
        logging.info("Loading %.2f%%", progress)

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
            try:
                trend_product_price_box = item.find_element(By.XPATH, './/div[contains(@class, "product-price")]')
                trend_product_price = trend_product_price_box.find_element(By.XPATH, './/div[contains(@class, "prc-box-dscntd")]').text
            except Exception as e:
                trend_product_price = "0"
                print("Couldn't get price", e)
        if trend_product_price != 0:
            trend_product_price = trend_product_price.replace("TL", "")
            trend_product_price = trend_product_price.replace(",", ".")
            trend_product_price = trend_product_price.strip()

        # get links
        try:
            trend_product_link = item.find_element(By.XPATH, './/div[contains(@class, "p-card-chldrn-cntnr")]/a').get_property('href')
            trend_link_list.append(trend_product_link)
        except Exception as e:
            trend_product_link = "0"
            trend_link_list.append(trend_product_link)
            print("Couldn't get link", e)
        
                #create a product object
        new_product = Product(trend_product_desc, trend_product_price, trend_product_link, "0", "000" ,trend_product_rating_count, "0", "0", "Trendyol")
        if trend_product_price == "0":
            continue
        trend_product_list.append(new_product)

    # product pages        
    for j, link in enumerate(trend_link_list):
        if j == product_number:
            break
        browser.get(link)

        #wait for max 10 seconds to load the page
        WebDriverWait(browser, 5).until(
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
            trend_product_merchant_name = browser.find_element(By.XPATH, '//div[contains(@class, "seller-name-text")]').text
            trend_product_merchant_rating_box = browser.find_element(By.XPATH, '//div[contains(@class, "product-seller-line")]')
        except Exception as e:
            trend_product_merchant_name = "0"
            print("Couldn't get merchant name", e)

        try:    
            trend_product_merchant_rating = trend_product_merchant_rating_box.find_element(By.XPATH, './/div[contains(@class, "sl-pn")]').text
        except Exception as e:
            trend_product_merchant_rating = "0"
            print("Couldn't get merchant", e)

        # get rating
        try:
            # trend_product_rating_box = browser.find_element(By.XPATH, '//div[contains(@class, "product-detail-container")]')
            rating = browser.find_element(By.XPATH, '//div[contains(@class, "pr-rnr-sm-p")]/span').text
            # print("qqqqqqqqqqqqqqqqqqqq", rating)
        except Exception as e:
            rating = "0"
            print("Couldn't get rating", e)

        #create a merchant object
        new_merchant = Merchant(trend_product_merchant_name, trend_product_merchant_rating, trend_product_img)
        trend_merchant_list.append(new_merchant)
        trend_rating_list.append(rating)

    for i, item in enumerate(trend_product_list):
        item.name = brand.capitalize() + " " + item.name
        trproduct = Product(item.name, item.price, item.link, trend_merchant_list[i].image, trend_rating_list[i], item.rating_count, trend_merchant_list[i].name, trend_merchant_list[i].rating, item.website)
        trend_temp_list.append(trproduct)

 
    browser.quit()    
    end = time.time()
    print("The time of execution of Trendyol script is :",
      (end-start) * 10**3, "ms")

    search_query_split = search_query.lower().split(" ")
    print(search_query_split)
    for i in trend_temp_list:
        name_split = remove_punctuation(i)
        # print(name_split)
        is_add = True
        for j in search_query_split:
            if j in name_split:
                continue
            else:
                # print(j, "is not present in", i.name)
                is_add = False
        if is_add:
            # print("Added", i.name)
            trend_product_list_main.append(i)
        
    

def amazon(amazon_product_list_main, brand, search_query):
    product_number = 8
    print("Starting Amazon")
    start = time.time()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--enable-gpu')
    chrome_options.add_argument('disable-notifications')

    service_obj = Service(rf"C:\Users\ahmet\AppData\Local\Programs\Python\Python39\chromedriver.exe")

    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])


    browser = webdriver.Chrome('chromedriver.exe', options=chrome_options, service=service_obj)
    browser.maximize_window()


    browser.get('https://www.amazon.com.tr/s?k=' + search_query)
    delay = 5

    WebDriverWait(browser, delay).until(EC.element_to_be_clickable(("xpath", '//*[@id="sp-cc-accept"]')))

    # WebDriverWait(browser, delay).until(EC.presence_of_element_located(("xpath", '//*[@id="sp-cc-accept"]')))
    logging.info("Amazon Cookies Accepted")

    # Click on the cookies button
    browser.find_element("xpath", '//*[@id="sp-cc-accept"]').click()

    # browser.implicitly_wait(2)
    WebDriverWait(browser, delay).until(EC.presence_of_element_located(("xpath", '//*[@id="brandsRefinements"]')))

    amazon_brand_filters = browser.find_element(By.ID, 'brandsRefinements').find_element(By.CLASS_NAME, 'a-unordered-list').get_property('children')
    
    #Select the brand
    for i in amazon_brand_filters:
        brand_name = i.find_element(By.CLASS_NAME, 'a-list-item').find_element(By.CLASS_NAME, 'a-link-normal').find_element(By.CLASS_NAME, 'a-size-base').text
        logging.debug("brands %s", brand_name)
        if i.text.lower() == brand.lower():
            i.find_element(By.CLASS_NAME, 'a-list-item').find_element(By.CLASS_NAME, 'a-link-normal').click()
            break
    
   
    product_link = []
    amazon_temp_list = []
    amazon_product_list = []
    amazon_merchant_list = []
    items = WebDriverWait(browser,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
    for j, item in enumerate(items):
        if j ==product_number:
            break
        #Get descriptions
        amazon_product_desc = item.find_element(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]')

        # Find price
        amazon_whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
        # amazon_fraction_price = item.find_elements(By.XPATH,'.//span[@class="a-price-fraction"]') # we dont need fraction

        if amazon_whole_price != []:
            price = amazon_whole_price[0].text
        else:
            price = 0
        
        if price == 0:
            continue

        #get rratings
        amazon_rating_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

        if amazon_rating_box != []:
            amazon_ratings = amazon_rating_box[0].get_attribute('aria-label')
            amazon_ratings = str(amazon_ratings.split(" ")[-1]).replace(",",".")
            amazon_rating_num = amazon_rating_box[1].get_attribute('aria-label')
        else:
            amazon_ratings = 0
            amazon_rating_num = 0


        #get links
        amazon_product_link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute('href')
        product_link.append(amazon_product_link)

        amazon_product_image = item.find_element(By.XPATH, './/img[@class="s-image"]').get_attribute('src')

        new_product = Product(amazon_product_desc.text, price, amazon_product_link, amazon_product_image, amazon_ratings, amazon_rating_num, "0", "0", "Amazon")
        amazon_product_list.append(new_product)

    for i, link in enumerate(product_link):
        if i == product_number:
            break
        browser.get(link)

        WebDriverWait(browser, delay).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="merchant-info"]')))

        #Get merchant info
        try:
            merchant_info = browser.find_elements(By.XPATH, './/div[@id="merchant-info"]/a')

            if len(merchant_info) != 0:
                merchant_name = merchant_info[0].text
            else:
                merchant_name = "Amazon.com.tr"   

        except:
            merchant_name = "Amazon.com.tr"   
        
        new_merchant = Merchant(merchant_name, 0, 0)
        amazon_merchant_list.append(new_merchant)

    for i, item in enumerate(amazon_product_list):
        product_obj = Product(item.name, item.price, item.link, item.image, item.rating, item.rating_count, amazon_merchant_list[i].name, amazon_merchant_list[i].rating, item.website)
        amazon_temp_list.append(product_obj)


    browser.quit()
    end = time.time()
    print("The time of execution of Amazon script is :",
      (end-start) * 10**3, "ms")


    # Remove the products that do not contain the search_query
    search_query_split = search_query.lower().split(" ")
    for i in amazon_temp_list:
        name_split = remove_punctuation(i)
        is_add = True
        for j in search_query_split:
            if j in name_split:
                continue
            else:
                is_add = False
        if is_add:
            amazon_product_list_main.append(i)





if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--arg1', type=str, help='Description of argument 1')
    parser.add_argument('--arg2', type=str, help='Description of argument 2')
    args = parser.parse_args()
    

    #Replace + with space
    search_query = args.arg1.replace("+", " ")
    brand = args.arg2.replace("+", " ")

    print("Search query: ", search_query)
    print("Brand:", brand)

    manager = mp.Manager()
    trendyol_product_list_main = manager.list()
    amazon_product_list_main = manager.list()

    trendyol_process = mp.Process(target=trendyol,args=(trendyol_product_list_main, brand,search_query))
    trendyol_process.start()

    amazon_process = mp.Process(target=amazon, args=(amazon_product_list_main, brand,search_query))
    amazon_process.start()

    trendyol_process.join()
    amazon_process.join()

    f = open("amazon.txt", "wb")
    for i in amazon_product_list_main:
        f.write((json.dumps(i.__dict__, ensure_ascii=False)).encode('utf8'))
        f.write("\n".encode('utf-8'))
    f.close()

    
    f = open("trendyol.txt", "wb")
    for i in trendyol_product_list_main:
        f.write((json.dumps(i.__dict__, ensure_ascii=False)).encode('utf8'))
        f.write("\n".encode('utf-8'))
    f.close()

    # Trendyol Grouping
    matched_products = []
    matched_products_index = -1
    SIMILARITY_RATE = 0.80

    while len(trendyol_product_list_main) != 0:

        max_product = 0
        max_length = 0
        max_product_index = 999
        
        for counter, i in enumerate(trendyol_product_list_main):
            if len(i.name) > max_length:
                max_length = len(i.name)
                max_product = i
                max_product_index = counter

        matched_products_index += 1
        matched_products.append([])

        trendyol_product_list_main.pop(max_product_index)
        to_be_removed = []

        ever_matched = False
        for counter, i in enumerate(trendyol_product_list_main):
            matched = match_similar(max_product, i, SIMILARITY_RATE)
            if matched:
                matched_products[matched_products_index].append(i)
                to_be_removed.append(counter)
                ever_matched = True
                
        remove_item = sorted(to_be_removed, reverse=True)

        for i in remove_item:
            removeditem = trendyol_product_list_main.pop(i)
            # print("removed", removeditem.name, "\n")

        matched_products[matched_products_index].append(max_product)

    # for counter, i in enumerate(matched_products):
    #     print("Group", counter )
    #     for j in i:
    #         print(j.name)


    # Match amazon products with trendyol groups 
    for i in range(0, len(matched_products)):
        max_product_of_current_group = matched_products[i][-1]
        to_be_removed = []
        for counter, item in enumerate(amazon_product_list_main):
            is_matched = match_similar(max_product_of_current_group, item, SIMILARITY_RATE)
            if is_matched:
                matched_products[i].append(item)
                to_be_removed.append(counter)

        for k in sorted(to_be_removed, reverse=True):
            amazon_product_list_main.pop(k)



    # Move the products with no match to a separate list 
    to_be_removed = []
    no_match = []
    for i, group in enumerate(matched_products):
        if len(group) == 1:
            to_be_removed.append(i)
            no_match.append(group[0])

    for i in sorted(to_be_removed, reverse=True):
        matched_products.pop(i)

    # Append the products with no match to the end of the no match list
    for i in amazon_product_list_main:
        no_match.append(i)

    matched_products_with_formula = []


    print("before no match groups")
    for counter, i in enumerate(matched_products):
        print("\nGroup", counter )
        for j in i:
            print(j.name)

    print("\nNo Match")
    for i in no_match:
        print(i.name, i.merchant_name)


    # Regroup the products with no match
    matched_products_index = len(matched_products) - 1

    for i in no_match:
        max_product = 0
        max_length = 0
        max_product_index = 999

        for counter, i in enumerate(no_match):
            if len(i.name) > max_length:
                max_length = len(i.name)
                max_product = i
                max_product_index = counter

        matched_products_index += 1
        matched_products.append([])

        no_match.pop(max_product_index)
        to_be_removed = []

        ever_matched = False
        for counter, i in enumerate(no_match):
            matched = match_similar(max_product, i, 0.70)
            if matched:
                matched_products[matched_products_index].append(i)
                to_be_removed.append(counter)
                ever_matched = True
                
        remove_item = sorted(to_be_removed, reverse=True)

        for i in remove_item:
            removeditem = no_match.pop(i)
            # print("removed", removeditem.name, "\n")

        matched_products[matched_products_index].append(max_product)






    # Move the products with no match to a separate list 
    to_be_removed = []
    for i, group in enumerate(matched_products):
        if len(group) == 1:
            to_be_removed.append(i)
            no_match.append(group[0])

    for i in sorted(to_be_removed, reverse=True):
        matched_products.pop(i)





    print("After no match groups")
    for counter, i in enumerate(matched_products):
        print("\nGroup", counter )
        for j in i:
            print(j.name)

    print("\nNo Match")
    for i in no_match:
        print(i.name, i.merchant_name)






    matched_products_with_formula = []

    # Use the formula to order items
    for i in matched_products:
        for j in i:
            temp_price = int(str(j.price).replace(".", ""))

            if str(j.merchant_rating) == "0":
                j.merchant_rating = 8.0

            if j.merchant_name == "Amazon.com.tr":
                j.merchant_rating = 10.0

            j.formula_rank = float(temp_price) * 0.4 - float(j.rating_count) * 0.3 + float(j.rating) * 0.2 + float(j.merchant_rating) * 0.1
            
        templist = sorted(i, key=lambda x: x.formula_rank, reverse=True)
        matched_products_with_formula.append(templist)

    no_match_with_formula = []    
    # Use formula to order no match
    for i in no_match:
        temp_price = int(str(i.price).replace(".", ""))

        if str(i.merchant_rating) == "0":
            i.merchant_rating = 8.0

        i.formula_rank = float(i.rating_count) * 0.3 + float(i.rating) * 0.2 + float(i.merchant_rating) * 0.1 - float(temp_price) * 0.4

    no_match_with_formula = sorted(no_match, key=lambda x: x.formula_rank, reverse=True)
        
    no_match_amazon = []
    no_match_trendyol = []

    for i in no_match_with_formula:
        if i.website == "Amazon":
            no_match_amazon.append(i)
        else:
            no_match_trendyol.append(i)

    no_match_trendyol = sorted(no_match_trendyol, key=lambda x: x.formula_rank, reverse=True)
    no_match_amazon = sorted(no_match_amazon, key=lambda x: x.formula_rank, reverse=True)
    group_labels = []

    for counter, i in enumerate(matched_products_with_formula):
        min_length_item = {"item": "", "length": 999, "counter": 99}
        tempgroups = [z for z in i]

        for counter, j in enumerate(tempgroups):
            current_product = remove_punctuation(j)
            # print(current_product)
            if len(current_product) < min_length_item["length"]:
                min_length_item["length"] = len(current_product)
                min_length_item["item"] = j
                min_length_item["counter"] = counter

        tempgroups.pop(min_length_item["counter"])
        label_item = remove_punctuation(min_length_item["item"])
        temp_label_item = label_item
        for item in tempgroups:
            current_product = remove_punctuation(item)

            
            to_be_removed = []
            for index, word in enumerate(label_item):
                if word in current_product:
                    pass
                else:
                    to_be_removed.append(index)
            
            remove_item = sorted(to_be_removed, reverse=True)
            for i in remove_item:
                removeditem = label_item.pop(i)

        label_item = [x.capitalize() for x in label_item]            
        label_item = " ".join(label_item)
        group_labels.append({"name": label_item})
    print("\n\n\n#################################################")
    for counter, i in enumerate(matched_products_with_formula):
        print("Group", counter, ":\n")
        for j in i:
            print(j.name,"  Rank: ", j.formula_rank ,"\n")

    print("Products with no match: \n")
    for i in no_match:
        print(i.name, "\n")

    f = open("groups.txt", "wb")
    for i in matched_products_with_formula:
        for j in i:
            f.write((json.dumps(j.__dict__, ensure_ascii=False)).encode('utf8'))
            f.write("\n".encode('utf-8'))
        f.write("###\n".encode('utf-8'))
    f.close()

    f = open("no_groups_amazon.txt", "wb")
    for i in no_match_amazon:    
        f.write((json.dumps(i.__dict__, ensure_ascii=False)).encode('utf8'))
        f.write("\n".encode('utf-8'))
    f.close()

    f = open("no_groups_trendyol.txt", "wb")
    for i in no_match_trendyol:    
        f.write((json.dumps(i.__dict__, ensure_ascii=False)).encode('utf8'))
        f.write("\n".encode('utf-8'))
    f.close()

    f = open("labels.txt", "wb")
    for i in group_labels:    
        f.write((json.dumps(i, ensure_ascii=False)).encode('utf8'))
        f.write("\n".encode('utf-8'))
    f.close()
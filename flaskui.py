from flask import Flask, redirect, request, url_for 
from flask import render_template
import subprocess
import json


DATA_PREFIX = "./data/"

app = Flask(__name__)

class Merchant:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating


def LoadProducts():
    f = open(DATA_PREFIX + "amazon.txt", "r", encoding="utf-8")
    amazontxt = f.readlines()
    f.close()

    aproducts = []
    for i in amazontxt:
        jsonstr = json.loads(i)
        aproducts.append(jsonstr)


    f = open(DATA_PREFIX + "trendyol.txt", "r", encoding="utf-8")
    trendyoltxt = f.readlines()
    f.close()

    tproducts = []
    for i in trendyoltxt:
        tproducts.append(json.loads(i))

    f = open(DATA_PREFIX + "groups.txt", "r", encoding="utf-8")
    groups = f.readlines()
    f.close()

    matched = [[]]
    matched_index = 0
    for counter, i in enumerate(groups):
        if counter == len(groups)- 1:
            break
        if i == "###\n":
            matched.append([])
            matched_index += 1
            continue
        matched[matched_index].append(json.loads(i))

    
    
    f = open(DATA_PREFIX + "no_groups_amazon.txt", "r", encoding="utf-8")
    no_groups = f.readlines()
    f.close()

    not_matched_amazon = []
    for counter, i in enumerate(no_groups):

        not_matched_amazon.append(json.loads(i))

    for i in not_matched_amazon:
        print(i["name"], "\n")

    f = open(DATA_PREFIX + "no_groups_trendyol.txt", "r", encoding="utf-8")
    no_groups = f.readlines()
    f.close()

    not_matched_trendyol = []
    for counter, i in enumerate(no_groups):

        not_matched_trendyol.append(json.loads(i))

    for i in not_matched_trendyol:
        print(i["name"], "\n")

    f = open(DATA_PREFIX + "labels.txt", "r", encoding="utf-8")
    no_groups = f.readlines()
    f.close()

    labels = []
    for counter, i in enumerate(no_groups):

        labels.append(json.loads(i))

    return matched, not_matched_amazon, not_matched_trendyol, labels


@app.route('/')
def welcome():
    return render_template('_base.html')

@app.route('/search', methods=['POST'])
def search():
  query = request.form['query']
  brand = request.form['brand']
  # Do something with the query here, such as storing it in a database or using it to search for something
  return redirect(url_for('index', query=query, brand=brand))

@app.route('/index')
def index():
    search_query = request.args.get('query')
    brand = request.args.get('brand')
    # Use the query here to search for something or display it to the user
    search_query = search_query.replace(" ", "+")
    brand = brand.replace(" ", "+")
    subprocess.call(f'python main.py --arg1 {search_query} --arg2 {brand}', shell=True)

    matched, not_matched_amazon, not_matched_trendyol, labels = LoadProducts()

    return render_template('_index.html', matched=matched, not_matched_amazon=not_matched_amazon, not_matched_trendyol=not_matched_trendyol, labels=labels)

@app.route('/order', methods=['GET', 'POST'])
def order():
    matched, not_matched_amazon, not_matched_trendyol, labels = LoadProducts()
    ordering_method = request.args.get('order')

    if ordering_method == "lowest":
        for i in matched:
            i.sort(key=lambda x: int(x["price"].replace(".", "")))

    elif ordering_method == "highest":
        for i in matched:
            i.sort(key=lambda x: int(x["price"].replace(".", "")), reverse=True) 

    elif ordering_method == "rating":
        for i in matched:
            i.sort(key=lambda x: x["rating"], reverse=True)      
    
    elif ordering_method == "comment":
        for i in matched:
            i.sort(key=lambda x: (x["comments"]["positive_count"] + x["comments"]["negative_count"]), reverse=True)
    
    elif ordering_method == "recommended":
        matched, not_matched_amazon, not_matched_trendyol, labels = LoadProducts()


    return render_template('_index.html', matched=matched, not_matched_amazon=not_matched_amazon, not_matched_trendyol=not_matched_trendyol, labels=labels)

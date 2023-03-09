from flask import Flask, redirect, request, url_for 
from flask import render_template
import subprocess
import json
import redis
from redis_namespace import StrictRedis

app = Flask(__name__)

DATA_PREFIX = "./data/"

class Merchant:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

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

    try:
        pass
        redis_connection = redis.StrictRedis()
        trendyol_redis = StrictRedis(namespace='Trendyol:')
        amazon_redis = StrictRedis(namespace='Amazon:')
        tr_cache = trendyol_redis.get(search_query).decode('utf-8')
        am_cache = amazon_redis.get(search_query).decode('utf-8')

        if tr_cache != None and am_cache != None:
            print("Cache hit")
            # return render_template('_index.html', matched=json.loads(tr_cache), not_matched_amazon=json.loads(am_cache), not_matched_trendyol=[], labels=[])
    except:
        pass
    # Use the query here to search for something or display it to the user
    search_query = search_query.replace(" ", "+")
    brand = brand.replace(" ", "+")
    subprocess.call(f'python main.py --arg1 {search_query} --arg2 {brand}', shell=True)
    #subprocess.call(["python", "main.py", "--arg1", search_query, "--arg2", brand])

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


    return render_template('_index.html', matched=matched, not_matched_amazon=not_matched_amazon, not_matched_trendyol=not_matched_trendyol, labels=labels)
from flask import Flask, redirect, request, url_for 
from flask import render_template
import subprocess
import json

app = Flask(__name__)

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
    # Use the query here to search for something or display it to the user
    search_query = search_query.replace(" ", "+")
    brand = brand.replace(" ", "+")
    subprocess.call(f'python main.py --arg1 {search_query} --arg2 {brand}', shell=True)
    #subprocess.call(["python", "main.py", "--arg1", search_query, "--arg2", brand])

    f = open("amazon.txt", "r", encoding="utf-8")
    amazontxt = f.readlines()
    f.close()

    aproducts = []
    for i in amazontxt:
        jsonstr = json.loads(i)
        aproducts.append(jsonstr)


    f = open("trendyol.txt", "r", encoding="utf-8")
    trendyoltxt = f.readlines()
    f.close()

    tproducts = []
    for i in trendyoltxt:
        tproducts.append(json.loads(i))

    f = open("groups.txt", "r", encoding="utf-8")
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

    
    
    f = open("no_groups.txt", "r", encoding="utf-8")
    no_groups = f.readlines()
    f.close()

    not_matched = []
    for counter, i in enumerate(no_groups):
        if counter == len(no_groups)- 1:
            break
        not_matched.append(json.loads(i))

    # print("From Flask\n")
    # for counter, i in enumerate(matched):
    #     print("Group", counter, ":\n")
    #     for j in i:
    #         print(j["name"], "\n")

    return render_template('_index.html', matched=matched, not_matched=not_matched)
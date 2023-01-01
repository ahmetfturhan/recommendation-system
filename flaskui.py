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
    return render_template('base.html')

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
        jsonstr = json.loads(i)
        tproducts.append(jsonstr)

    return render_template('index.html', aproducts = aproducts, tproducts = tproducts)
    
    
    # eski flaskui.py kodlarÄ±
    
    #search_query = "iphone 11"
    #search_query = search_query.replace(" ", "+")

    #brand = "apple"
    #brand = brand.replace(" ", "+")
    #subprocess.call(f'python main.py {search_query} {brand}', shell=True)

    #f = open("amazon.txt", "r", encoding="utf-8")
    #amazontxt = f.readlines()
    #f.close()

    #aproducts = []
    #for i in amazontxt:
        #jsonstr = json.loads(i)
        #aproducts.append(jsonstr)

    
    #f = open("trendyol.txt", "r", encoding="utf-8")
    #trendyoltxt = f.readlines()
    #f.close()

    #tproducts = []
    #for i in trendyoltxt:
        #jsonstr = json.loads(i)
        #tproducts.append(jsonstr)

    #return render_template('welcomePage.html', aproducts = aproducts, tproducts = tproducts)
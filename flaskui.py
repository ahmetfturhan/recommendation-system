from flask import Flask
from flask import render_template
import subprocess
import json

app = Flask(__name__)

class Merchant:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

@app.route('/')
def index():
    search_query = "iphone 11"
    search_query = search_query.replace(" ", "+")

    brand = "apple"
    brand = brand.replace(" ", "+")
    subprocess.call(f'python main.py {search_query} {brand}', shell=True)

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
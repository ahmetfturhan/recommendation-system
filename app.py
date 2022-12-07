from flask import Flask
from flask import render_template
import subprocess

app = Flask(__name__)

class Merchant:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

@app.route('/')
def index():
    search_query = "iphone 11"
    brand = "apple"
    p = subprocess.Popen(['python', 'main.py', '--search_query', search_query, '--brand', brand], stdout=subprocess.PIPE)


    m = Merchant('John', 4.5)
    m1 = Merchant('Ahmet', 31224)
    plist = [m, m1]
    aproducts = []
    [aproducts.append(x.__dict__) for x in plist]

    m2 = Merchant('QWE', 41235)
    m3 = Merchant('Asdaset', 3121)
    plist = [m2, m3]
    tproducts = []
    [tproducts.append(x.__dict__) for x in plist]

    return render_template('index.html', aproducts = aproducts, tproducts = tproducts)
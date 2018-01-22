"""
from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask(__name__)

@app.route("/")
def index():
    return "Flask App!"

@app.route("/hello/<string:name>/")
def hello(name):
    return render_template(
        'test.html',name=name[::-1])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

"""
from lxml import html
from pyaqadvisor import Tank, Stocking
from BeautifulSoup import BeautifulSoup
import urllib2
from flask import Flask, url_for, request, jsonify
import requests
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'

@app.route('/aqadvisor')
def aqadvisor_api():
    stocking = Stocking().add('cardinal tetra', 5)\
                         .add('panda cory', 6)\
                         .add('lemon_tetra', 12)\
                         .add('pearl gourami', 4)

    #print "My user-specified stocking is: ", stocking
    #print "I translate this into: ", stocking.aqadvisor_stock_list


    t = Tank('55g').add_filter("AquaClear 30").add_stocking(stocking)
    #print "Aqadvisor tells me: ",
    #print t.get_stocking_level()
    #string = (str(t.get_stocking_level()))
    #lines = string.split('\n')
    stocking_stats = str(t.get_stocking_level())
    j = {
        "speech": stocking_stats,
        "displayText": stocking_stats,
        "data": {},
        "contextOut": [],
        "source": "DuckDuckGo"
    }
    return jsonify(j)
    #print soup.get_text()
    #return "a"

"""@app.route('/parse')
def parse_api():
    page = urllib2.urlopen('http://127.0.0.1:5000/aqadvisor')
    soup = BeautifulSoup(page, 'html.parser')
    return soup.get_text()"""


if __name__ == '__main__':
    app.run()

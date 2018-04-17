from flask import Flask, jsonify, request, make_response
from pyaqadvisor import Tank, Stocking
import re
import json

app = Flask(__name__, static_url_path = "")

@app.route('/', methods=['GET'])
def index():
    return "Yo, it's working!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    if req.get("result").get("action") == "webhookTest":
    	res = testWebhook(req)
    elif req.get("result").get("action") == "FishList":
        stocking = makeStocking(req)
        res = testStocking(stocking)
    elif req.get("result").get("action") == "getSpecs":
        res = getSpecs(req)
    else:
        res = {}
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return res

def getSpecs(req):
    fishList = req.get("result").get("parameters").get("fishnum")
    stocking = Stocking()
    for fish in fishList:
        stocking.add(fish.get("fish"), fish.get("number"))
    tankSize = req.get("result").get("parameters").get("gallons")
    tankFilter = req.get("result").get("parameters").get("filter")
    t = Tank(tankSize).add_filter(tankFilter).add_stocking(stocking)
    stocking_stats = t.get_stocking_level()
    return parse(stocking_stats)

def makeStocking(req):
    fishList = req.get("result").get("parameters").get("number-of-fish")
    stocking = Stocking()
    for fish in fishList:
        stocking.add(fish.get("fish"), fish.get("number"))
    return stocking

def testStocking(stocking):
    t = Tank('55g').add_filter('AquaClear 30').add_stocking(stocking)
    stocking_stats = t.get_stocking_level()
    return parse(stocking_stats)

def testWebhook(req):
    stocking = Stocking().add('cardinal tetra', 5)\
                        .add('panda cory', 6)\
                        .add('lemon_tetra', 12)\
                        .add('pearl gourami', 4)

    tankSize = req.get("result").get("parameters").get("gallons")
    tankFilter = req.get("result").get("parameters").get("filter")
    t = Tank(tankSize).add_filter(tankFilter).add_stocking(stocking)
    stocking_stats = t.get_stocking_level()
    return parse(stocking_stats)

@app.route('/test2', methods=['GET'])
def test2():
    return "hello"

@app.route('/test', methods=['GET'])
def aquadvisor():
    stocking = Stocking().add('cardinal tetra', 5)\
                        .add('panda cory', 6)\
                        .add('lemon_tetra', 12)\
                        .add('pearl gourami', 4)

    t = Tank('55g').add_filter("AquaClear 30").add_stocking(stocking)
    stocking_stats = t.get_stocking_level()
    return stocking_stats

def parse(stats):
    bold = re.findall(r'<b>(.*?)</b>', stats)
    speech = "Your aquarium filtration capacity is " + bold[0] + ". " + bold[2] + "."
    return {
        "speech":speech,
        "displayText": speech,
        "data": stats,
        "contextOut": [],
        "source": "rocky-lowlands-15066"
    }

if __name__ == "__main__":
	port = 9001
	app.run(host='0.0.0.0', port=port)

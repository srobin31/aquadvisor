from flask import Flask, jsonify, request, make_response
from pyaqadvisor import Tank, Stocking
import re

app = Flask(__name__, static_url_path = "")

@app.route('/', methods=['GET'])
def index():
    return "Yo, it's working!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return res

def processRequest(req):
    stocking = Stocking().add('cardinal tetra', 5)
    filter = req.get("result").get("parameters").get("filter")
    t = Tank('55g').add_filter(filter).add_stocking(stocking)
    aquadvisor = t.get_stocking_level()
    return parse(aquadvisor)

@app.route('/test', methods=['GET', 'POST'])
def aquadvisor():
    stocking = Stocking().add('cardinal tetra', 5)\
                        .add('panda cory', 6)\
                        .add('lemon_tetra', 12)\
                        .add('pearl gourami', 4)

    t = Tank('55g').add_filter("AquaClear 30").add_stocking(stocking)
    stocking_stats = t.get_stocking_level()
    return stocking_stats

def parse(req):
    bold = re.findall(r'<b>(.*?)</b>', stats)
    speech = "Your aquarium filtration capacity is " + bold[0] + ". " + bold[2] + "."
    return {
        "speech":speech,
        "displayText": speech,
        "data": req,
        "contextOut": [],
        "source": "rocky-lowlands-15066"
    }

if __name__ == "__main__":
	port = 9001
	app.run(host='0.0.0.0', port=port)

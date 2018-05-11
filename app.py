from flask import Flask, jsonify, request, make_response
from pyaqadvisor import Tank, Stocking
import re
import json

app = Flask(__name__, static_url_path = "")

class info():
    def __init__(self):
        self._ranges = None
        self._bold = None
        self._warnings = None

    @property
    def ranges(self):
        return self._ranges

    @property
    def bold(self):
        return self._bold

    @property
    def warnings(self):
        return self._warnings

    @ranges.setter
    def ranges(self, value):
        self._ranges = value

    @bold.setter
    def bold(self, value):
        self._bold = value

    @warnings.setter
    def warnings(self, value):
        self._warnings = value

information = info()

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    action = req.get("result").get("action")

    if action == "callApi":
        res = callApi(req)
    elif action == "getRanges":
        res = getRanges()
    # elif action == "getStats":
    #     res = getStats(req)
    # elif action == "getWarnings":
    #     res = getWarnings(req)
    else:
        res = {}
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return res

def callApi(req):
    fishList = req.get("result").get("parameters").get("fishnum")
    stocking = Stocking()
    for fish in fishList:
        stocking.add(fish.get("fish"), fish.get("number"))
    tankSize = req.get("result").get("parameters").get("gallons")
    tankFilter = req.get("result").get("parameters").get("filter")
    t = Tank(tankSize).add_filter(tankFilter).add_stocking(stocking)
    api_response = t.get_stocking_level()
    return parse(api_response)

def parse(api_response):
    # information = info()
    information.ranges = re.findall(r'range:(.*?)</font>', api_response)
    stats = re.search('Your aquarium filtration.*\\.', api_response)
    information.bold = re.findall(r'<b>(.*?)</b>', stats.group(0))

    filtCap = information.bold[0][:-1]

    information.warnings = re.findall(r'<li>(.*?)</li>', api_response)
    for warning in information.warnings:
        warning = re.sub(r'<.*?>', '', warning)

    speech = "Say \"ranges\" for your recommended temperature and pH ranges.\nSay \"stats\" for your stocking level and filtration capacity.\nWe also found " + str(len(information.warnings)) + " warnings. Say \"warnings\" to see them."

    return {
        "speech": speech,
        "displayText": speech,
        "data": api_response,
        "contextOut": [],
        "source": "rocky-lowlands-15066"
    }

def getRanges():
    r = information.ranges
    #speech = "Your recommended temperature range is" + r[0] + ".\nYour recommended pH range is " + r[1] "."
    speech = str(r[0])
    return {
        "speech": speech,
        "displayText": speech,
        "data": r,
        "contextOut": [],
        "source": "rocky-lowlands-15066"
    }

def filtCapHelp(filtCap, speech):
    if filtCap < 90:
        speech += "Because your filtration capacity is less than 90%, we recommend that you get a more powerful filter."
    elif filtCap > 90 and filtCap < 110:
        speech += "Because your filtration capacity is around 100%, you have an okay filter. If you add more fish, we recommend upgrading to a stronger filter."
    else:
        speech += "Because your filtration capacity is above 110%, you're in good shape. However, you'll want to check again if you add more fish."

    return speech

if __name__ == "__main__":
	port = 9001
	app.run(host='0.0.0.0', port=port)

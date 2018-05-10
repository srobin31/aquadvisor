from flask import Flask, jsonify, request, make_response
from pyaqadvisor import Tank, Stocking
import re
import json

app = Flask(__name__, static_url_path = "")

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    if req.get("result").get("action") == "getSpecs":
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

def parse(api_response):
    information = info()
    information.ranges = re.findall(r'range:(.*?)</font>', api_response)
    stats = re.search('Your aquarium filtration.*\\.', api_response)
    information.bold = re.findall(r'<b>(.*?)</b>', stats.group(0))

    filtCap = information.bold[0][:-1]

    information.warnings = re.findall(r'<li>(.*?)</li>', info)
    for warning in information.warnings:
        warning = re.sub(r'<.*?>', '', warning)

    speech = "You have " + information.warnings.length " warnings."

    return {
        "speech": speech,
        "displayText": speech,
        "data": api_response,
        "contextOut": [],
        "source": "rocky-lowlands-15066"
    }

def filtCapHelp(filtCap):
    if filtCap < 90:
        speech += "Because your filtration capacity is less than 90%, we recommend that you get a more powerful filter."
    elif filtCap > 90 and filtCap < 110:
        speech += "Because your filtration capacity is around 100%, you have an okay filter. If you add more fish, we recommend upgrading to a stronger filter."
    else:
        speech += "Because your filtration capacity is above 110%, you're in good shape. However, you'll want to check again if you add more fish."

class info():
    def __init__(self):
        self._ranges = None
        self._bold = None
        self._warnings = None
        self._speech = None

    @property
    def ranges(self):
        """I'm the 'x' property."""
        return self._ranges

    @property
    def bold(self):
        """I'm the 'x' property."""
        return self._bold

    @property
    def warnings(self):
        """I'm the 'x' property."""
        return self._warnings

    @property
    def speech(self):
        """I'm the 'x' property."""
        return self._speech

    @speech.setter
    def speech(self, value):
        #print("setter of x called")
        self._speech = value

    @ranges.setter
    def ranges(self, value):
        #print("setter of x called")
        self._ranges = value

    @bold.setter
    def bold(self, value):
        #print("setter of x called")
        self._bold = value

    @warnings.setter
    def warnings(self, value):
        #print("setter of x called")
        self._warnings = value

if __name__ == "__main__":
	port = 9001
	app.run(host='0.0.0.0', port=port)

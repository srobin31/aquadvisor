from flask import Flask, jsonify, request, make_response
from pyaqadvisor import Tank, Stocking
import re
import json

app = Flask(__name__, static_url_path = "")

# class tankInfo():
#     def __init__(self):
#         self._size = None
#         self._filter = None
#         self._stocking = None
#
#     @property
#     def size(self):
#         return self._size
#
#     @property
#     def filter(self):
#         return self._filter
#
#     @property
#     def stocking(self):
#         return self._stocking
#
#     @size.setter
#     def size(self, value):
#         self._size = value
#
#     @filter.setter
#     def filter(self, value):
#         self._filter = value
#
#     @stocking.setter
#     def stocking(self, value):
#         self._stocking = value

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
    elif action == "getStats":
        res = getStats()
    elif action == "getWarnings":
        res = getWarnings()
    # elif action == "addFish":
    #     res = addFish(req)
    else:
        res = {}
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return res

def callApi(req):
    # myTank = tankInfo()
    myStocking = Stocking()

    fishList = req.get("result").get("parameters").get("fishnum")
    for fish in fishList:
        myStocking.add(fish.get("fish"), fish.get("number"))
    stocking = myStocking

    tankSize = req.get("result").get("parameters").get("gallons")
    tankFilter = req.get("result").get("parameters").get("filter")
    t = Tank(tankSize).add_filter(tankFilter).add_stocking(stocking)
    api_response = t.get_stocking_level()
    return parse(api_response)

# def addFish(req):
#     fishList = req.get("result").get("parameters").get("fishnum")
#     for fish in fishList:
#         myStocking.add(fish.get("fish"), fish.get("number"))
#     myTank.stocking = myStocking
#
#     t = Tank(myTank.size).add_filter(myTank.filter).add_stocking(myTank.stocking)
#     api_response = t.get_stocking_level()
#     return parse(api_response)

def parse(api_response):
    information.ranges = re.findall(r'range:(.*?)</font>', api_response)
    stats = re.search('Your aquarium filtration.*\\.', api_response)
    information.bold = re.findall(r'<b>(.*?)</b>', stats.group(0))
    information.warnings = re.findall(r': (.*?)</li>', api_response)

    speech = "Say \"ranges\" for your recommended temperature and pH ranges.\nSay \"stats\" for your stocking level and filtration capacity.\nWe also found " + str(len(information.warnings)) + " warnings. Say \"warnings\" to see them."

    return makeJson(speech, api_response)

def getRanges():
    r = information.ranges
    speech = "Your recommended temperature range is" + str(r[0]) + "\nYour recommended pH range is " + str(r[1])
    return makeJson(speech, r)

def getStats():
    b = information.bold
    filtCap = b[0][:-1]
    speech = b[1] + "."
    speech += "\n\nYour aquarium filtration capacity is " + filtCap + "%. " + filtCapHelp(int(filtCap))
    return makeJson(speech, b)

def getWarnings():
    w = information.warnings
    speech = ""
    for warning in information.warnings:
        warning = re.sub(r'<.*?>', '', warning)
        speech += ""+warning+"\n"
    return makeJson(speech, w)

def filtCapHelp(filtCap):
    speech = ""
    if filtCap < 90:
        speech += "Because your filtration capacity is less than 90%, we recommend that you get a more powerful filter."
    elif filtCap > 90 and filtCap < 110:
        speech += "Because your filtration capacity is around 100%, you have an okay filter. If you add more fish, we recommend upgrading to a stronger filter."
    else:
        speech += "Because your filtration capacity is above 110%, you're in good shape. However, you'll want to check again if you add more fish."

    return speech

def makeJson(speech, data):
    return {
        "speech": speech,
        "displayText": speech,
        "data": data,
        "contextOut": [],
        "source": "rocky-lowlands-15066"
    }

if __name__ == "__main__":
	port = 9001
	app.run(host='0.0.0.0', port=port)

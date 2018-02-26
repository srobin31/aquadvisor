from flask import Flask, jsonify, request, make_response
from pyaqadvisor import Tank, Stocking
import re

import json

app = Flask(__name__, static_url_path = "")

@app.route('/webhook', methods=['GET', 'POST'])
def index():
    req = request.get_json(silent=True, force=True)
    print(req)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = parse(aquadvisor())
	#
    # res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#@app.route('/aquadvisor', methods=['GET', 'POST'])
def aquadvisor():
    stocking = Stocking().add('cardinal tetra', 5)\
                         .add('panda cory', 6)\
                         .add('lemon_tetra', 12)\
                         .add('pearl gourami', 4)

    t = Tank('55g').add_filter("AquaClear 30").add_stocking(stocking)
    stocking_stats = t.get_stocking_level()
    return stocking_stats

#@app.route('/parsed', methods=['GET', 'POST'])
def parse(api_stats):
    bold = re.findall(r'<b>(.*?)</b>', api_stats)
    speech = "Your aquarium filtration capacity is " + bold[0] + ". " + bold[2] + "."
	# return jsonify(
	# 	{
	# 		"speech":speech,
    #         "displayText": speech,
    #         "data": {},
    #         "contextOut": [],
    #         "source": ""
	# 		# "text":stats,
	# 		# "type":type(stats).__name__,
	# 		# "bold":bold,
	# 		# "speech":speech,
	# 		# "level":bold[2]
	# 	}
	# )
    return speech

# @app.route('/unparsed', methods=['GET', 'POST'])
# def unparsed():
#     stats = aquadvisor()
#     return jsonify(
#         {
#             "speech":stats,
#             "displayText": stats,
#             "data": {},
#             "contextOut": [],
#             "source": ""
#         }
#     )

if __name__ == "__main__":
	port = 9001
	app.run(host='0.0.0.0', port=port)

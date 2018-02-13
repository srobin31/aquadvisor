from flask import Flask, jsonify
from pyaqadvisor import Tank, Stocking
import re

app = Flask(__name__, static_url_path = "")

@app.route('/', methods=['GET', 'POST'])
def index():
	return "Yo, it's working!"

@app.route('/test', methods=['GET', 'POST'])
def aquadvisor():
    stocking = Stocking().add('cardinal tetra', 5)\
                         .add('panda cory', 6)\
                         .add('lemon_tetra', 12)\
                         .add('pearl gourami', 4)

    t = Tank('55g').add_filter("AquaClear 30").add_stocking(stocking)
    stocking_stats = t.get_stocking_level()
    return stocking_stats

@app.route('/parsed', methods=['GET', 'POST'])
def parsed():
	stats = aquadvisor()
	bold = re.findall(r'<b>(.*?)</b>', stats)
	return jsonify(
		{
			"text":stats,
			"type":type(stats).__name__,
			"bold":bold
		}
	)

@app.route('/json', methods=['GET', 'POST'])
def json():
    stats = aquadvisor()
    return jsonify(
        {
            "speech":stats,
            "displayText": stats,
            "data": {},
            "contextOut": [],
            "source": ""
        }
    )

if __name__ == "__main__":
	app.run()

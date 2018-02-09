from flask import Flask, jsonify
from pyaqadvisor import Tank, Stocking
app = Flask(__name__, static_url_path = "")
@app.route('/')
def index():
	return "Yo, it's working!"

@app.route('/test')
def aquadvisor():
    stocking = Stocking().add('cardinal tetra', 5)\
                         .add('panda cory', 6)\
                         .add('lemon_tetra', 12)\
                         .add('pearl gourami', 4)

    t = Tank('55g').add_filter("AquaClear 30").add_stocking(stocking)
    stocking_stats = t.get_stocking_level()
    return stocking_stats

@app.route('/json')
def json():
    return jsonify(
        {
            "speech":aquadvisor(),
            "displayText": aquadvisor(),
            "data": {},
            "contextOut": [],
            "source": "DuckDuckGo"
        }
    )

if __name__ == "__main__":
	app.run()
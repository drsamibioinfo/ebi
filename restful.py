#!/usr/bin/env python3.8
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/date", methods=['GET'])
def get():
    import pytz
    from datetime import datetime
    tz = pytz.timezone('Europe/London')
    date_str = datetime.now(tz=tz).strftime("%a %b %d %H:%M:%S %Z %Y")
    return jsonify({
        "date": date_str
    })


if __name__ == '__main__':
    print("Starting Restful Server running on all interfaces with port : 8000 " )
    app.run(host="0.0.0.0", port=8000)

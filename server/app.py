#!/usr/bin/env -S python3 -m flask run
from pprint import pprint
from flask import Flask
from flask import request as requests

app = Flask(__name__)

ALL_MSGS = []

@app.route("/")
def hello_world():
    return "<p>English or Spanish?</p>"

@app.route("/send", methods=["POST", "GET"])
def send():
    error = None
    if requests.method == "POST":
        data = requests.form.to_dict()
        ALL_MSGS.append(data)
        print(requests.form["time"])
        print(requests.form["hash"])
        print(requests.form["msg"])
        return "200"
    return "<h1>Hello.</h1>"

@app.route("/receive", methods=["GET"])
def receive():
    args = requests.args
    requested_index = args.get("current", default=0, type=int) # 0 indexed
    return ALL_MSGS[requested_index:len(ALL_MSGS)] # return all messages from the requested to the latest.

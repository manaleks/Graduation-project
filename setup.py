# -*- coding: utf8 -*-
import os
from flask import Flask, request, render_template


app = Flask(__name__)

def main_page():
    return render_template('main.html')
def simple_text(num):
    return "Hello!" + str(num)

rules = []
rules.append({"rule":'/',"name":"main_page","method":main_page})
rules.append({"rule":'/simple_text/<num>',"name":"simple_text","method":simple_text})
for rule in rules:
    app.add_url_rule(rule["rule"], rule["name"], rule["method"])


@app.route('/favicon.ico', methods=['GET', 'POST'])
def game():
    return "Hello!"


if __name__ == "__main__":
    app.run(debug=True)
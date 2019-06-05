# -*- coding: utf8 -*-
import os
from flask import Flask, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

# GAME
@app.route('/', methods=['GET', 'POST'])
def game():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()

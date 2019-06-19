import requests
from PIL import Image
from io import BytesIO

import os
import sys
import shutil
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import send_from_directory
from werkzeug.utils import secure_filename

root_dir = sys.path[0]
ready_images_dir = os.path.join(sys.path[0],'ready_images')

# recreate inputs
if os.path.isdir(ready_images_dir):
    shutil.rmtree(ready_images_dir)
os.mkdir(ready_images_dir)

app = Flask(__name__)

MODELS = ["dora-marr-network", "starry-night-network",
"la_muse.ckpt","rain_princess.ckpt","scream.ckpt",
"udnie.ckpt","wave.ckpt", "wreck.ckpt"]

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
         #   flash('No file part')
            return render_template('main.html', models=MODELS, info_mess='No selected file')
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return render_template('main.html', models=MODELS, info_mess='No selected filename')
        filename = file.filename

        print(type(file))
        print(file)
        print(filename)

        # image processing
        url = 'http://180a7fd8.ngrok.io/'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        #file_to_load_open = open('static/images/bricks.jpg', 'rb')
        #print(file_to_load_open)
        #print(type(file_to_load_open))

        files = {'file': file}
        r = requests.post(url, headers=headers, files=files)

        # save ready image
        print(r)
        print(type(r))
        print(type(r.text))
        print(r.text)
        print(type(r.content))
        i = Image.open(BytesIO(r.content))
        print(type(i))
        print(i)

        file_path = os.path.join(ready_images_dir,filename)

        print(file_path)

        i.save(file_path)

        return render_template('main.html', models=MODELS, info_mess='all_ok', filename=filename)

    return render_template('main.html', models=MODELS, info_mess='')


@app.route('/video_feed/<filename>')
def video_feed(filename):
    return send_from_directory(ready_images_dir, filename)

# Icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


"""
            url = 'https://f16dfe47.ngrok.io/'
            #files = {'file': open('static/images/bricks.jpg', 'rb')}
            files = {'file': open('static/images/bricks.jpg', 'rb')}
            r = requests.post(url, files=files)

            print(r)
            print(type(r))
            print(type(r.text))
            print(type(r.content))

            i = Image.open(BytesIO(r.content))
            i.show()

            print(i)
            print(type(i))
"""
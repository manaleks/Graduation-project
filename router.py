import os
import sys
import shutil

from flask import Flask
from flask import Response
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import send_from_directory
from werkzeug.utils import secure_filename

import requests
from io import BytesIO
from PIL import Image
import base64
import json


root_dir = sys.path[0]
upload_images_dir = os.path.join(sys.path[0],'upload_images_dir')
ready_images_dir = os.path.join(sys.path[0],'ready_images_dir')

# recreate upload_images_dir
if os.path.isdir(upload_images_dir):
    shutil.rmtree(upload_images_dir)
os.mkdir(upload_images_dir)
# recreate ready_images_dir
if os.path.isdir(ready_images_dir):
    shutil.rmtree(ready_images_dir)
os.mkdir(ready_images_dir)

app = Flask(__name__)


MODELS2 = [ {"model":"dora-marr-network", "jpg":"dora-maar-picasso.jpg", "name":"Dora Maar Picasso"},
            {"model":"starry-noght-network", "jpg":"starry_night.jpg", "name":"Starry Night"},
            {"model":"scream.ckpt", "jpg":"scream.jpg", "name":"Scream"},
            {"model":"la_muse.ckpt", "jpg":"la_muse.jpg", "name":"La Muse"},
            {"model":"udnie.ckpt", "jpg":"udnie.jpg", "name":"Udnie"},
            {"model":"wave.ckpt", "jpg":"wave.jpg", "name":"Wave"},
            {"model":"wreck.ckpt", "jpg":"wreck.jpg", "name":"Wreck"},
            {"model":"rain_princess.ckpt", "jpg":"rain_princess.jpg", "name":"Rain princess"}
            ]  

MODELS = ["dora-marr-network", "starry-night-network",
"la_muse.ckpt","rain_princess.ckpt","scream.ckpt",
"udnie.ckpt","wave.ckpt", "wreck.ckpt"]

def getModels():
    return json.dumps(MODELS2, default=str)

# SERV
@app.route('/', methods=['GET', 'POST'])
def server_work():
    if request.method == 'POST':

        if 'file' not in request.files:
            return json.dumps({'error': 'No selected file'})
        file = request.files['file']

        if file.filename == '':
            return json.dumps({'error': 'No selected file'})

        filename = file.filename

        print(type(file))
        print(file)
        print(filename)


        # Get new folder num
        upload_list = os.listdir(upload_images_dir)
        print(upload_list)

        if len(upload_list) == 0:
            image_number = 0
        else:
            image_number = int(max([int(x) for x in upload_list])) + 1
        print(image_number)

        # Create upload folder
        input_folder_path = os.path.join(upload_images_dir,str(image_number))
        print(input_folder_path)
        os.mkdir(input_folder_path)

        # if the are this dir
        output_folder_path = os.path.join(ready_images_dir,str(image_number))
        if os.path.isdir(output_folder_path):
            shutil.rmtree(output_folder_path)

        # Create outload folder
        print(output_folder_path)
        os.mkdir(output_folder_path)


        # save upload file
        upload_file_path = os.path.join(input_folder_path,filename)
        file.save(upload_file_path)


        # prepare image processing
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        # get file
        file_to_load_open = open(upload_file_path, 'rb')
        print(file_to_load_open)
        print(type(file_to_load_open))
        files = {'file': file_to_load_open}

        # make url
        url = 'https://c6bc0db6.ngrok.io/'


        # get model_name
        model_name = request.form.get('models')
        print(model_name)

        if model_name:
            # Set used model on top
            MODELS.remove(model_name)
            MODELS.insert(0, model_name)
        else:
            model_name = MODELS[0]
        print(model_name)

        #model_url = url + str(model)
        #print(model_url)

        # image processing
        r = requests.post(url, headers=headers, files=files, data = {'models':model_name})

        # save ready image
        print(r)
        print(type(r))
        print(type(r.text))
        # print(r.text)
        print(type(r.content))
        i = Image.open(BytesIO(r.content))
        print(type(i))
        print(i)

        ready_file_path = os.path.join(output_folder_path,filename)

        print(ready_file_path)

        i.save(ready_file_path)
        
        print(filename)
        file_extension = filename.split('.')[-1]
        print(filename.split('.')[-1])
        print(file_extension)

        # ready_im = Image.open(file_path)
        img_data = open(ready_file_path, 'rb' ).read()
        # bytes_im = base64.b64encode(ready_im.tobytes())
        img_data = "data:image/" + file_extension + ";base64," + base64.b64encode(img_data).decode()

        return json.dumps({'data': img_data})

        #return render_template('main.html', models=MODELS, info_mess='all_ok', image_number=image_number, filename=filename)

    return render_template('main.html', models=MODELS, info_mess='')

@app.route('/models', methods=['GET', 'POST'])
def get_models():
    return Response(getModels(), mimetype="text/event-stream")

# Icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/run_hello')
def run_hello():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.post("https://manaleks.herokuapp.com/hello", headers=headers, data = {'models':'SUPERHELLO'})

    # save ready image
    print(r)
    print(type(r))
    print(type(r.text))
    print(r.text)
    print(type(r.content))

    return r.text


@app.route('/hello', methods=['POST'])
def hello():

    try:
        model = request.args.get('models')
        print('hello get: '+ str(model))
    except:
        print("dont work: model = request.args.get('models')")

    try:
        model = request.form.get('models')
        print('hello get: '+ str(model))
    except:
        print("dont work: model = request.args.get('models')")

    return 'hello: ' + str(model)



import os
from flask import Flask 
from flask import Response
from flask import request
from flask import redirect
from flask import url_for   
from flask import render_template
from flask import send_from_directory
from werkzeug.utils import secure_filename

from utils import list_files
from evaluate import ffwd_different_dimensions

import shutil
from PIL import Image
import base64
import json

app = Flask(__name__)

############################################################################################################

import sys
BASE_FOLDER = sys.path[0]

UPLOAD_FOLDER = '{}/inputs'.format(BASE_FOLDER)
OUTLOAD_FOLDER = '{}/results'.format(BASE_FOLDER)
CHECKPOINT = '{}/models/'.format(BASE_FOLDER)

# recreate inputs
if os.path.isdir(UPLOAD_FOLDER):
    shutil.rmtree(UPLOAD_FOLDER)
os.mkdir(UPLOAD_FOLDER)
# recreate results
if os.path.isdir(OUTLOAD_FOLDER):
    shutil.rmtree(OUTLOAD_FOLDER)
os.mkdir(OUTLOAD_FOLDER)


MODELS2 = [ {"model":"dora-marr-network", "jpg":"dora-maar-picasso.jpg", "name":"Dora Maar Picasso"},
            {"model":"starry-night-network", "jpg":"starry_night.jpg", "name":"Starry Night"},
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

count_quota = []

file_folder_number = 0

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
BATCH_SIZE = 4
DEVICE = '/gpu:0'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTLOAD_FOLDER'] = OUTLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getModels():
    return json.dumps(MODELS2, default=str)

# SERV
@app.route('/', methods=['GET', 'POST'])
def server_work():
    if request.method == 'POST':
        work_type = request.form.get('work_type')
        if work_type == 'serv':
            # check if the post request has the file part
            if 'file' not in request.files:
                return json.dumps({'error': 'No selected file'})
                
            file = request.files['file']

            if file.filename == '':
                return json.dumps({'error': 'No selected file'})

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                        
                # Get new folder num
                upload_list = os.listdir(UPLOAD_FOLDER)
                print(upload_list)

                if len(upload_list) == 0:
                    new_upload_num = 0
                else:
                    new_upload_num = int(max([int(x) for x in upload_list])) + 1
                print(new_upload_num)

                # Create upload folder
                input_folder_path = os.path.join(UPLOAD_FOLDER,str(new_upload_num))
                os.mkdir(input_folder_path)

                # if the are this dir
                output_folder_path = os.path.join(OUTLOAD_FOLDER,str(new_upload_num))
                if os.path.isdir(output_folder_path):
                    #os.rmdir(output_folder_path) 
                    shutil.rmtree(output_folder_path)

                # Create outload folder
                print(new_upload_num)
                os.mkdir(output_folder_path)

                # add new file
                path_to_save = os.path.join(app.config['UPLOAD_FOLDER'],str(new_upload_num))
                file.save(os.path.join(path_to_save, filename))
                
                print('start')
                get_model = request.form.get('models')
                print(get_model)

                if get_model:
                    model = get_model
                    # Set used model on top
                    MODELS.remove(model)
                    MODELS.insert(0, model)
                else:
                    model = MODELS[0]

                #return json.dumps({'model': model, 'image_number': new_upload_num, 'filename': filename})
                return redirect(url_for('get_file', model=model, image_number=new_upload_num, filename=filename))
        else:
            # check if the post request has the file part
            if 'file' not in request.files:
                return json.dumps({'error': 'No selected file'})

            file = request.files['file']
            if file.filename == '':
                return json.dumps({'error': 'No selected file'})

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                        
                # Get new folder num
                upload_list = os.listdir(UPLOAD_FOLDER)
                print(upload_list)

                if len(upload_list) == 0:
                    new_upload_num = 0
                else:
                    new_upload_num = int(max([int(x) for x in upload_list])) + 1
                print(new_upload_num)

                # Create upload folder
                input_folder_path = os.path.join(UPLOAD_FOLDER,str(new_upload_num))
                os.mkdir(input_folder_path)

                # if the are this dir
                output_folder_path = os.path.join(OUTLOAD_FOLDER,str(new_upload_num))
                if os.path.isdir(output_folder_path):
                    #os.rmdir(output_folder_path) 
                    shutil.rmtree(output_folder_path)

                # Create outload folder
                print(new_upload_num)
                os.mkdir(output_folder_path)

                # add new file
                path_to_save = os.path.join(app.config['UPLOAD_FOLDER'],str(new_upload_num))
                file.save(os.path.join(path_to_save, filename))
                
                print('start')
                get_model = request.form.get('models')
                print(get_model)

                if get_model:
                    model = get_model
                    # Set used model on top
                    MODELS.remove(model)
                    MODELS.insert(0, model)
                else:
                    model = MODELS[0]

                return json.dumps({'model': model, 'image_number': new_upload_num, 'filename': filename})
                #return redirect(url_for('get_file', model=model, image_number=new_upload_num, filename=filename))

    return render_template('main_style.html', models=MODELS, info_mess='')


@app.route('/uploads/<model>/<image_number>/<filename>', methods=['GET', 'POST'])
def get_file(filename,image_number,model):

    # check count quota
    if len(count_quota) > 0:
        # return render_template('main.html', models=MODELS, info_mess='sorry, quota is 2. Check after second')
        return json.dumps({'error': 'Sorry, quota is 2. Check after second'})


    # chech image resolution
    folder_path = os.path.join(UPLOAD_FOLDER,str(image_number))
    image_path = os.path.join(folder_path,str(filename))
    im = Image.open(image_path)
    width, height = im.size
    print(width)
    print(height)
    if width + height > 3500:
        # return render_template('main.html', models=MODELS, info_mess='sorry, this file is too big')
        return json.dumps({'error': 'sorry, this file is too big'})

    # add count
    count_quota.append(1)

    # get new folders for this photo
    new_file_path = os.path.join(UPLOAD_FOLDER,str(image_number))
    ready_file_path = os.path.join(OUTLOAD_FOLDER,str(image_number))

    files = list_files(new_file_path)
    full_in = [os.path.join(new_file_path,x) for x in files]
    full_out = [os.path.join(ready_file_path,x) for x in files]
    print(full_out)
    checkpoint = CHECKPOINT + model
    print(checkpoint)
    ffwd_different_dimensions(full_in, full_out, checkpoint, device_t=DEVICE,
                    batch_size=BATCH_SIZE)
    
    if len(count_quota) > 0:
        count_quota.pop(0)

    return send_from_directory(ready_file_path, filename)


@app.route('/style/<model>/<image_number>/<filename>', methods=['GET', 'POST'])
def get_file_style(filename,image_number,model):

    # check count quota
    if len(count_quota) > 0:
        # return render_template('main.html', models=MODELS, info_mess='sorry, quota is 2. Check after second')
        return json.dumps({'error': 'Sorry, quota is 2. Check after second'})


    # chech image resolution
    folder_path = os.path.join(UPLOAD_FOLDER,str(image_number))
    image_path = os.path.join(folder_path,str(filename))
    im = Image.open(image_path)
    width, height = im.size
    print(width)
    print(height)
    if width + height > 3500:
        # return render_template('main.html', models=MODELS, info_mess='sorry, this file is too big')
        return json.dumps({'error': 'sorry, this file is too big'})

    # add count
    count_quota.append(1)

    # get new folders for this photo
    new_file_path = os.path.join(UPLOAD_FOLDER,str(image_number))
    ready_file_path = os.path.join(OUTLOAD_FOLDER,str(image_number))

    files = list_files(new_file_path)
    full_in = [os.path.join(new_file_path,x) for x in files]
    full_out = [os.path.join(ready_file_path,x) for x in files]
    print(full_out)
    checkpoint = CHECKPOINT + model
    print(checkpoint)
    ffwd_different_dimensions(full_in, full_out, checkpoint, device_t=DEVICE,
                    batch_size=BATCH_SIZE)
    
    if len(count_quota) > 0:
        count_quota.pop(0)

    print(filename)
    file_extension = filename.split('.')[-1]
    print(filename.split('.')[-1])
    print(file_extension)

    file_path = os.path.join(ready_file_path,filename)
    # ready_im = Image.open(file_path)
    img_data = open(file_path, 'rb' ).read()
    # bytes_im = base64.b64encode(ready_im.tobytes())
    img_data = "data:image/" + file_extension + ";base64," + base64.b64encode(img_data).decode()

    return json.dumps({'data': img_data})

    # return send_from_directory(ready_file_path, filename)
    



@app.route('/images/<filename>', methods=['GET', 'POST'])
def get_image(filename):
    return send_from_directory(BASE_FOLDER+'/static/images/', filename)

@app.route('/models', methods=['GET', 'POST'])
def get_models():
    return Response(getModels(), mimetype="text/event-stream")


# Icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')



if __name__ == "__main__":
    app.run(debug=True, port=5000)

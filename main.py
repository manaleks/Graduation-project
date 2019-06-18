import os
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import send_from_directory
from werkzeug.utils import secure_filename

from utils import list_files
from evaluate import ffwd_different_dimensions

app = Flask(__name__)

############################################################################################################

import sys
BASE_FOLDER = sys.path[0]

UPLOAD_FOLDER = '{}/inputs'.format(BASE_FOLDER)
OUTLOAD_FOLDER = '{}/results'.format(BASE_FOLDER)
CHECKPOINT = '{}/models/'.format(BASE_FOLDER)

MODELS = ["dora-marr-network","rain-princess-network", "starry-night-network",
"la_muse.ckpt","rain_princess.ckpt","scream.ckpt",
"udnie.ckpt","wave.ckpt", "wreck.ckpt"]                    


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
BATCH_SIZE = 4
DEVICE = '/gpu:0'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTLOAD_FOLDER'] = OUTLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# SERV
@app.route('/', methods=['GET', 'POST'])
def server_work():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
         #   flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
          #  flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # delete files
            files = list_files(UPLOAD_FOLDER)
            for file_name in files:
                os.unlink(os.path.join(UPLOAD_FOLDER,file_name))

            # add new file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            model = request.form['models']
            # Set used model on top
            MODELS.remove(model)
            MODELS.insert(0, model)


            return redirect(url_for('get_file',
                                    filename=filename, model=model))

    return render_template('server_work.html', models=MODELS)


@app.route('/uploads/<filename>/<model>', methods=['GET', 'POST'])
def get_file(filename,model):
    files = list_files(UPLOAD_FOLDER)
    full_in = [os.path.join(UPLOAD_FOLDER,x) for x in files]
    full_out = [os.path.join(OUTLOAD_FOLDER,x) for x in files]
    print(full_out)
    checkpoint = CHECKPOINT + model
    print(checkpoint)
    ffwd_different_dimensions(full_in, full_out, checkpoint, device_t=DEVICE,
                    batch_size=BATCH_SIZE)

    # delete files
    for file_name in files:
        os.unlink(os.path.join(UPLOAD_FOLDER,file_name))

    print(filename)

    return send_from_directory(app.config['OUTLOAD_FOLDER'], filename)

@app.route('/video_feed/<param>/<folder>')
def video_feed(param,folder):
    print(folder)
    print(param)
    return send_from_directory('/home/manaleks/Graduation-project/static/images', 'chicago.jpg')

@app.route('/video_feed2')
def video_feed2():
    return send_from_directory('/home/manaleks/Graduation-project/static/images', 'chicago.jpg')


# JS
@app.route('/client_work', methods=['GET', 'POST'])
def client_work():
    return render_template('index.html')


@app.route('/images/<filename>', methods=['GET', 'POST'])
def get_image(filename):
    return send_from_directory(BASE_FOLDER+'/static/images/', filename)


# Icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(port=5005)

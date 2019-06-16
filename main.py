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
CHECKPOINT = '{}/models/la_muse.ckpt'.format(BASE_FOLDER)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
BATCH_SIZE = 4
DEVICE = '/gpu:0'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTLOAD_FOLDER'] = OUTLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
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
            
            return redirect(url_for('uploaded_file',
                                    filename=filename))
            
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    files = list_files(UPLOAD_FOLDER)
    full_in = [os.path.join(UPLOAD_FOLDER,x) for x in files]
    full_out = [os.path.join(OUTLOAD_FOLDER,x) for x in files]
    ffwd_different_dimensions(full_in, full_out, CHECKPOINT, device_t=DEVICE,
                    batch_size=BATCH_SIZE)

    # delete files
    for file_name in files:
        os.unlink(os.path.join(UPLOAD_FOLDER,file_name))

    print(filename)

    return send_from_directory(app.config['OUTLOAD_FOLDER'], filename)


############################################################################################################


############################################################################################################
# JS module

@app.route('/js', methods=['GET', 'POST'])
def game():
    return render_template('index.html')

############################################################################################################


if __name__ == "__main__":
    app.run()
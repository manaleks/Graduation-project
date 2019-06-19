import requests
from PIL import Image
from io import BytesIO

import os
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for   
from flask import render_template
from flask import send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

MODELS = ["dora-marr-network", "starry-night-network",
"la_muse.ckpt","rain_princess.ckpt","scream.ckpt",
"udnie.ckpt","wave.ckpt", "wreck.ckpt"]     

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
            return render_template('server_work.html', models=MODELS, info_mess='No selected file')
            #return redirect(url_for('server_work', models=MODELS, info_mess='No selected file'))
            #return redirect(request.url)


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

            return 'hello'

    return render_template('server_work.html', models=MODELS, info_mess='')

# Icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(port=5006)

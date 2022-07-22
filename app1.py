from __future__ import division, print_function

import os


import numpy as np

# Keras
from keras.utils import load_img,img_to_array
import tensorflow as tf

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename


# Define a flask app
app = Flask(__name__)




def model_predict(img_path, model):
    img =load_img(img_path, target_size=(224,224,3))



    
    x = img_to_array(img)

    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)


    str=""
    if preds[0][0]==1:
        str="Bacterial blight"
    elif preds[0][1]==1:
        str="Curl virus"
    elif preds[0][2]==1:
        str="Fussarium wilt"
    else:
        str="Healthy!"

    return str


@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        load_model= tf.keras.models.load_model('./cotton_model_version_2.h5')
        preds = model_predict(file_path,load_model)
     
        return render_template('result.html', name=preds)
    return None


if __name__ == '__main__':
    app.run(debug=True)

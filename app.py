from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
#For solving local object has no attribute
from tensorflow.keras.models import load_model
from keras.preprocessing import image
import base64

#Hack 1
# import keras.backend.tensorflow_backend as tb
# tb._SYMBOLIC_SCOPE.value = True

# Flask utils
from flask import Flask, redirect, url_for, request, render_template ,render_template_string
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

#For changing the template directory
# template_dir = os.path.dirname('./')+"/frontend"
# app = Flask(__name__, template_folder=template_dir)

import translate as tr

# Define a flask app
app = Flask(__name__)

#==================================================================Link Frontend with backend================================
                                                                # Check how to get the image
# Model saved with Keras model.save()
#MODEL_PATH = './models/resnet152_weights_tf.h5'
MODEL_PATH = './models/model_resnet152.h5'

#Load your trained model
model = load_model(MODEL_PATH)
model._make_predict_function()          # Necessary
print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
# from keras.applications.resnet import ResNet152
# model = ResNet152(weights='imagenet')
# model.save('./models/model_resnet152.h5')
print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    print("YOYOYO")
    #img = img.resize(224,224)
    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)
    print(x)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='caffe')

    preds = model.predict(x)
    return preds



@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        print("Chala re Namakool")
        #Get the file from post request
        f = request.form['data']
        #conversion into bytestring        
        f = bytes(f, 'utf-8') 
    
        #storing the data file
        with open("uploads/imageToSave.png", "wb") as fh:
            fh.write(base64.decodebytes(f))

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads','imageToSave.png' )
        # f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        result = str(pred_class[0][0][1])               # Convert to string
        result=result.replace("_"," ")                  # for removing _ from string
        print(result)
        print("Testing is the soul purpose")
        print(tr.translate(result,1))
        # return [tr.translate(result),result]
        return  '{} {} {}'.format(tr.translate(result,1),"-", result)
    return None


@app.route('/otherlang', methods=['GET', 'POST'])
def transLateTOOther():
    if request.method == 'POST':
        print("Chala re TRanslator")
        sen = request.form['sen']
        usecase = request.form['lan']
        print(sen," YO ",usecase)
        print(tr.translate(sen,usecase))

        return  '{}'.format(tr.translate(sen,usecase))
    return None




if __name__ == '__main__':
    app.run(debug=True)


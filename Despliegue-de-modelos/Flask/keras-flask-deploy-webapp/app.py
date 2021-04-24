import os
import sys

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# TensorFlow y tf.keras
import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

import numpy as np
from util import base64_to_pil

# Declaramos la aplicación flask
app = Flask(__name__)
model = MobileNetV2(weights='imagenet')
print('Modelo cargado. Visite la dirección http://127.0.0.1:5000/')


# Modelo guardado con Keras model.save()
MODEL_PATH = 'models/your_model.h5'

# Carga tu propio modelo entrenado
# model = load_model(MODEL_PATH)
# model._make_predict_function()          # Necessary
# print('Modelo cargado. Comenzando a servir...')


def model_predict(img, model):
    img = img.resize((224, 224))

    # Preprocesamos la imagen
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Tenga cuidado con la forma en que su modelo entrenado maneja la entrada
    # ¡De lo contrario, no hará una predicción correcta!
    x = preprocess_input(x, mode='tf')

    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Página principal
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Obtener la imagen del post request
        img = base64_to_pil(request.json)

        # Guardamos la imagen en ./uploads
        # img.save("./uploads/image.png")

        # Hacemos la predicción
        preds = model_predict(img, model)

        # Procesamos el resultado
        pred_proba = "{:.3f}".format(np.amax(preds))    # Probabilidad máxima 
        pred_class = decode_predictions(preds, top=1)   # ImageNet Decode

        result = str(pred_class[0][0][1])               # Convertimos a string
        result = result.replace('_', ' ').capitalize()
        
        # Serializamos el resultado, puede agregar campos adicionales
        return jsonify(result=result, probability=pred_proba)

    return None


if __name__ == '__main__':
    # app.run(port=5000, threaded=False)

    # Servimos la app con gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()

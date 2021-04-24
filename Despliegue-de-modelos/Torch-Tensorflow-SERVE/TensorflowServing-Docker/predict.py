import json

import matplotlib.pyplot as plt
import numpy as np
import requests
from tensorflow.keras.datasets.mnist import load_data

# Cargamos el dataset MNIST
(_, _), (x_test, y_test) = load_data()

# hacemos un reshape a los datos y lo pasamos a un solo canal
x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], x_test.shape[2], 1))
# normalizamos los pixeles
x_test = x_test.astype('float32') / 255.0


# URL donde se esta sirviendo el modelo
url = 'http://localhost:8501/v1/models/img_classifier:predict'

def make_prediction(instances):
   print("\nComenzando predicción\n")
   data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
   headers = {"content-type": "application/json"}
   json_response = requests.post(url, data=data, headers=headers)
   predictions = json.loads(json_response.text)['predictions']
   return predictions


n_predictions = 1000
predictions = make_prediction(x_test[0:n_predictions])

for i, pred in enumerate(predictions):
   if i % 100 == 0:
      print(f"Valor target: {y_test[i]}, Valor predicho: {np.argmax(pred)}")


acc = np.ones_like(y_test[0:n_predictions])
predictions = np.array(predictions)
acc = sum(acc[y_test[0:n_predictions] == np.argmax(predictions, axis=1)]) / n_predictions
print("\nAccuracy: ", acc)
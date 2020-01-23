""" Master Server """
import re
import base64
# from datetime import datetime
from io import BytesIO
import numpy as np
import tensorflow as tf
import ipfshttpclient
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify
from scipy.misc import imread
from skimage.transform import resize

# import matplotlib.pyplot as plt
print("Finished Imports")

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]iasdfffsd/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# from flask_ngrok import run_with_ngrok
# run_with_ngrok(app)

UPLOAD_DIR = "./upload_dir/"
current_model = ["model.h5"]

@app.route('/')
def hello():

  """ Welcome Page """

  return render_template("index.html")

@app.route('/predict/', methods=['GET', 'POST'])
def predict():

  """ Primary Prediction Endpoint """

  img_data = request.get_data()
  imgstr = re.search(b'base64,(.*)', img_data).group(1)
  image_bytes = base64.decodebytes(imgstr)
  image_stream = BytesIO(image_bytes)
  x = imread(image_stream, mode='L')
  x = np.invert(x)
  x = resize(x, (28, 28))
  img = np.reshape(x, (1, 28, 28))
  predictions = loaded_model.predict_classes(img)
  print(predictions)
  # plt.imshow(img.reshape((28, 28)))
  # plt.show()

  return str(predictions)

@app.route('/model/address', methods=['GET', 'POST'])
def model_address():

  """ Get Distributed Model Hash """

  res = client.add('model.h5', 'model.json')
  print(res)

  return jsonify(res)

@app.route('/model/', methods=['GET'])
def upload():

  """ Upload Page """

  return render_template("file_upload_form.html")

@app.route('/model/upload/', methods=['POST'])
def success():

  """ Upload Handler """

  f = request.files['file']
  # now = str(datetime.now())
  now = ""
  fn = str(f.filename).split(".")[0]
  fext = str(f.filename).split(".")[1]
  finalfn = secure_filename(f"{fn}{now}.{fext}")
  f.save(f"{UPLOAD_DIR}{finalfn}")
  current_model.append(str(UPLOAD_DIR+finalfn))

  return render_template("success.html", name=finalfn)

@app.route('/model/status/', methods=['GET'])
def model_status():

  """ Model Status """

  return render_template("status.html", model_name=current_model[-1])


if __name__ == '__main__':

  print("Loading Model")
  json_file = open('model.json', 'r')
  loaded_model_json = json_file.read()
  json_file.close()
  loaded_model = tf.keras.models.model_from_json(loaded_model_json)
  loaded_model.load_weights("model.h5")

  print("Model Loaded")
  loaded_model.compile(optimizer='adam',
                       loss='sparse_categorical_crossentropy',
                       metrics=['accuracy'])

  print("Model Compiled")

  print("Connecting to private swarm")
  ipfs_api = '/ip4/127.0.0.1/tcp/5001/http'
  client = ipfshttpclient.connect(addr=ipfs_api)
  print("Connected")

  app.run()

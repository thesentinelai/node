""" Local Node Server """
from os import getenv, path, makedirs
from random import randrange
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import ipfshttpclient
from web3 import Web3, HTTPProvider
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import tensorflow as tf
from contract import contractABI, contractAddress

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]iasdfffsd/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

ipfs_api = '/ip4/127.0.0.1/tcp/5001/http'
client = ipfshttpclient.connect(ipfs_api)
print(f"Connected to IPFS v{client.version()['Version']}")

active_tasks = []
Sentinel = ""


def addToIPFS(_fn="model.h5"):

  """ Add File to IPFS """

  res = client.add(_fn)
  return res['Hash']


def add_self_to_exchange():

  """ Add Server to Exchange """

  params = {
    'eth_address': getenv('ETHADDRESS'),
    'ip': getenv('NODE1_URL')
  }
  posturl = f"{getenv('COORDINATOR_URL')}{getenv('NODES_ENDPOINT')}"
  try:
    resp = requests.post(posturl, json=params)
  except:
    print("Coordinator Node is Offline")
    exit(0)

  if resp.status_code != 200:
    print("Coordinator Node is Offline")
    exit(0)
  else:
    print("Connected to Coordinator Node")


@app.route('/')
def server():

  """ Online Test """

  html = """<p style='font-family: monospace;padding: 10px;'>
            Local Training Node is online 🚀
            </p>"""

  return html


@app.route('/status')
def status():

  """ Returns server status """

  server_data = {
    "active_tasks": active_tasks
  }

  return jsonify(server_data), 200


@app.route('/start-training/', defaults={'task_id': 0}, methods=['GET', 'POST'])
@app.route('/start-training/<int:task_id>', methods=['GET', 'POST'])
def start_training(task_id):

  """ Training Start """

  if task_id < 1:
    return jsonify("Invalid Task"), 400
  else:
    active_tasks.append(task_id)
    return jsonify("Task Added"), 200


def background_trainer():

  """ Background Transaction Handler """

  for ind, val in enumerate(active_tasks):

    print(f"TRAINING MODEL FOR TASK {val}")
    model_hashes = Sentinel.functions.getTaskHashes(val).call()
    model_hashes = [x for x in list(model_hashes) if x.strip()]

    try:
      if (len(model_hashes) >= 1):

        print(f"Fetching {model_hashes[-1]} from IPFS")
        client.get(model_hashes[-1])
        new_model = tf.keras.models.load_model(model_hashes[-1])
        print(new_model.summary())
        new_model.fit(xtrain, ytrain, epochs=1, verbose=0)
        fn = f"model_storage/{randrange(1000, 99999)}.h5"
        new_model.save(fn)
        new_hash = addToIPFS(fn)
        print(f"TASKID:{val} Trained {new_hash}")

      else:
        print("Invalid Task")

    except:
      print("Error in Training Model")

    active_tasks.pop(ind)


if __name__ == '__main__':

  w3 = Web3(HTTPProvider('https://testnet2.matic.network'))
  if not w3.isConnected():
    print("Web3 Not Connected")
    exit(0)
  else:
    print(f'Connected to Web3 v{w3.api}')

  add_self_to_exchange()

  Sentinel = w3.eth.contract(address=contractAddress, abi=contractABI)

  sched = BackgroundScheduler(daemon=True)
  sched.add_job(background_trainer, "interval", seconds=10)
  sched.start()

  if not path.exists('model_storage'): makedirs('model_storage')

  mnist = tf.keras.datasets.mnist
  (xtrain, ytrain), (xtest, ytest) = mnist.load_data()
  xtrain = tf.keras.utils.normalize(xtrain, axis=1)
  xtest = tf.keras.utils.normalize(xtest, axis=1)
  print("Data Loaded")

  app.run(
      host="127.0.0.1",
      port="5005",
      debug=True,
      use_reloader=False,
      threaded=True)

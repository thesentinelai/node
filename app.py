""" Local Node Server """
from os import getenv, path, makedirs
import sys
import ssl
import shutil
import logging
from random import randrange
from pprint import pprint
from flask import Flask, jsonify, render_template
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
app.secret_key = b'_5#y2L"F4Q8z\n\xec]iasdfjfsd/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

ipfs_api = '/dns/ipfs.infura.io/tcp/5001/https'
client = ipfshttpclient.connect(ipfs_api)
print(f"Connected to IPFS v{client.version()['Version']}")

active_tasks = []
global sentinel_contract

# https://www.codegrepper.com/code-examples/python/unable+to+get+local+issuer+certificate+tensorflow
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def add_to_ipfs(fn="model.h5"):

  """ Add File to IPFS """

  res = client.add(fn)
  return res['Hash']


def connect_to_coor():

  """ Add Node to Coordinator """

  get_ip = requests.get('https://api.ipify.org/?format=json')
  node_ip = get_ip.json()['ip'];

  params = {
    'eth_address': getenv('ETHADDRESS'),
    'ip': f"{getenv(NODE_URL)}"
  }
  print('Connecting to Coordinator')
  pprint(params)
  posturl = f"{getenv('COORDINATOR_URL')}{getenv('NODES_ENDPOINT')}"
  try:
    resp = requests.post(posturl, json=params)
  except:
    print("Coordinator Node is Offline")
    sys.exit(0)

  if resp.status_code != 200:
    print("Coordinator Node is Offline")
    sys.exit(0)
  else:
    print("Connected to Coordinator Node")

@app.route('/')
@app.route('/index.html')
def index():
  get_ip = requests.get('https://api.ipify.org/?format=json')
  node_ip = get_ip.json()['ip'];
  return render_template('index.html', ip=f"{getenv(NODE_URL)}")


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
    model_hashes = sentinel_contract.functions.getTaskHashes(val).call()
    model_hashes = [x for x in list(model_hashes) if x.strip()]
    task_data = sentinel_contract.functions.SentinelTasks(val).call() # taskID, currentRound, totalRounds, cost

    if len(model_hashes) >= task_data[2]:
      print(f"TASKID:{val} is completed.")
    else:
      try:
        if len(model_hashes) >= 1:
          active_hash = model_hashes[-1]
          print(f"Fetching {active_hash} from IPFS")
          if not path.exists(f'model_storage/{active_hash}'):
            client.get(active_hash)
            shutil.move(active_hash, 'model_storage')
          new_model = tf.keras.models.load_model(f"model_storage/{active_hash}")
          print(new_model.summary())
          print("Now Training Model")
          new_model.fit(xtrain, ytrain, epochs=1, verbose=0)
          fn = f"model_storage/{randrange(1000, 99999)}.h5"
          new_model.save(fn)
          new_hash = add_to_ipfs(fn)
          shutil.move(fn, f'model_storage/{new_hash}')
          print(f"TASKID:{val} Trained {new_hash}")

          params = {
              'ethAddress': getenv('ETHADDRESS'),
              'modelHash': new_hash
          }
          url = f"{getenv('COORDINATOR_URL')}{getenv('NEXTRUN_ENDPOINT')}/{val}"
          try:
            requests.post(url, json=params)
          except:
            print(f"Coordinator Node is Offline while POSTING RESULT")
            print(params)

        else:
          print("Invalid Task")

      except:
        print("Error in Training Model")

    active_tasks.pop(ind)

# Start Initialization

w3 = Web3(HTTPProvider('https://betav2.matic.network'))
if not w3.isConnected():
  print("Web3 Not Connected")
  sys.exit(0)
else:
  print(f'Connected to Web3 v{w3.api}')

connect_to_coor()

sentinel_contract = w3.eth.contract(address=contractAddress, abi=contractABI)

sched = BackgroundScheduler(daemon=True)
sched.add_job(background_trainer, "interval", seconds=10)
sched.start()

if not path.exists('model_storage'): makedirs('model_storage')

mnist = tf.keras.datasets.mnist
(xtrain, ytrain), (xtest, ytest) = mnist.load_data()
xtrain = tf.keras.utils.normalize(xtrain, axis=1)
xtest = tf.keras.utils.normalize(xtest, axis=1)
print("Data Loaded")

# End Initialization

if __name__ != "__main__":

  gunicorn_logger = logging.getLogger('gunicorn.error')
  app.logger.handlers = gunicorn_logger.handlers
  app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':

  app.run(
    host="0.0.0.0",
    port=int(getenv('PORT', str(3000))),
    debug=False,
    use_reloader=False,
    threaded=True
  )

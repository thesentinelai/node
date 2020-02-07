from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from contract import contractABI, contractAddress
from web3 import Web3,HTTPProvider
from time import sleep
from dotenv import load_dotenv
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
from os import getenv
from urllib.parse import quote
import subprocess
import ipfshttpclient
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]iasdfffsd/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

ipfs_api = '/ip4/127.0.0.1/tcp/5001/http'
client = ipfshttpclient.connect(ipfs_api)
print(f"Connected to IPFS v{client.version()['Version']}")

active_tasks = []
global SERVER_STATUS
Sentinel = ""


def addToIPFS(_fn = "model.h5"):
  res = client.add(_fn)
  client.pin_ls(type='all')
  return res['Hash']


def add_self_to_exchange():
  PARAMS = {
    'eth_address': getenv('ETHADDRESS'),
    'ip': getenv('NODE1_URL')
  }
  resp = requests.post(f"{getenv('COORDINATOR_URL')}{getenv('NODES_ENDPOINT')}", json= PARAMS)
  if (resp.status_code != 200):
    print("Coordinator Node is Offline")
    exit(0)
  else:
    print("Connected to Coordinator Node")


@app.route('/')
def server():

  """ Online Test """

  return "<p style='font-family: monospace;padding: 10px;'>Local Training Node is online 🚀</p>"


@app.route('/status')
def status():

  """ Returns server status """

  server_data = {
  "status" : SERVER_STATUS,
    "active_tasks" : active_tasks
  }

  return jsonify(server_data), 200


@app.route('/start-training/', defaults={'task_id': 0}, methods = ['GET', 'POST'])
@app.route('/start-training/<int:task_id>', methods = ['GET', 'POST'])
def start_training(task_id):

  """ Training Start """

  if task_id < 1:
    return jsonify("Invalid Task"), 400
  else:
    active_tasks.append(task_id)
    return jsonify("Task Added"), 200


def background_trainer():

  """ Background Transaction Handler """

  for ind in range(len(active_tasks)):
    SERVER_STATUS = "TRAINING"
    print(f"TRAINING MODEL FOR TASK {active_tasks[ind]}")
    model_hashes = list(Sentinel.functions.getTaskHashes(active_tasks[ind]).call())
    print(model_hashes)
    if (len(model_hashes) > 1):
      try:
        new_model = tf.keras.models.load_model(model_hashes[-2])
      except:
        print("INVALID MODEL FOR TASK "+ str(active_tasks[ind]))
    else:
      print("INVALID MODEL HASH FOR TASK "+ str(active_tasks[ind]))

    active_tasks.pop(ind)
    SERVER_STATUS = "IDLE"


if __name__ == '__main__':
  w3 = Web3(HTTPProvider('https://testnet2.matic.network'))
  if not w3.isConnected():
    print("Web3 Not Connected")
    exit(0)

  add_self_to_exchange()

  Sentinel = w3.eth.contract(address=contractAddress,abi=contractABI)

  sched = BackgroundScheduler(daemon=True)
  sched.add_job(background_trainer, "interval", seconds=10)
  sched.start()

  app.run(host="127.0.0.1", port="5005", debug=True, use_reloader=False, threaded=True)

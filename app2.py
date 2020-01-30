from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import subprocess
from contract import contractABI, contractAddress
from web3 import Web3,HTTPProvider
from time import sleep
import ipfshttpclient
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from socket import gethostname, gethostbyname

app = Flask(__name__)
CORS(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]iasdfffsd/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

active_tasks = []
global SERVER_STATUS
Sentinel = ""

def addToIPFS(_fn = "model.h5"):
  res = client.add(_fn)
  client.pin_ls(type='all')
  return res['Hash']

def add_self_to_exchange():
  exchange_url = '/'
  endpoint = "/node-handler"
  hostname = gethostname()
  IPAddr = gethostbyname(hostname)
  resp = requests.post(f"{exchange_url}{endpoint}/{IPAddr}")


@app.route('/')
def server():

  """ Online Test """

  return "<p style='font-family: monospace;padding: 10px;'>Server is online 🚀</p>"


@app.route('/status')
def status():

  """ Returns server status """
  server_data = {
   "status" : SERVER_STATUS,
   "active_tasks" : active_tasks
  }

  return jsonify(server_data), 200


@app.route('/get-hash/', defaults={'task_id': 1})
@app.route('/get-hash/<int:task_id>')
def get_hash(task_id):

  """ Getmodel hash for latest task """

  task_id = str(task_id)
  proc = subprocess.run(["node", "./node-api/model-hash.js", task_id], capture_output=True)
  if (not proc.stderr):
    output_clean = str(proc.stdout.decode("utf-8")).replace("\n", "")
    return jsonify(output_clean.split(",")), 200
  else:
    return jsonify(str(proc.stderr)), 400


@app.route('/start-training/', defaults={'task_id': 0})
@app.route('/start-training/<int:task_id>')
def start_training(task_id):

  """ Training Start """
  if task_id < 1:
    return jsonify("Invalid Task"), 400
  else:
    active_tasks.push(task_id)


def background_trainer():
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

  # add_self_to_exchange();

  Sentinel = w3.eth.contract(address=contractAddress,abi=contractABI)

  sched = BackgroundScheduler(daemon=True)
  sched.add_job(background_trainer, "interval", seconds=10)
  sched.start()

  ipfs_api = '/ip4/127.0.0.1/tcp/5001/http'
  client = ipfshttpclient.connect(ipfs_api)

  app.run(host="127.0.0.1", port="5000", debug=True, use_reloader=False, threaded=True)

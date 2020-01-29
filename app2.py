from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]iasdfffsd/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

active_task = []

@app.route('/')
def server():

  """ Online Test """

  return "Server is online 🚀"

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

@app.route('/start-training')
def start_training():

  """ Training Start """

  return "start"


if __name__ == '__main__':

  app.run()

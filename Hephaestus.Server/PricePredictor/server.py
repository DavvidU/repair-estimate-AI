from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import subprocess
import json

app = Flask(__name__)
CORS(app)

def run_model_script(model_name, data):
    script_path = f"./PricePredictor/{model_name}_prediction.py"
    input_data = json.dumps(data)
    result = subprocess.run(['python', script_path, input_data], capture_output=True, text=True)
    output = json.loads(result.stdout)
    return output

@app.route('/model1-prediction', methods=['POST'])
def model1_prediction():
    data = request.json['dataframe_split']
    print(data)
    response = run_model_script('model1', data)
    return jsonify(response)

@app.route('/model2-prediction', methods=['POST'])
def model2_prediction():
    data = request.json
    response = run_model_script('model2', data)
    return jsonify(response)

@app.route('/model3-prediction', methods=['POST'])
def model3_prediction():
    data = request.json
    response = run_model_script('model3', data)
    return jsonify(response)

@app.route('/model4-prediction', methods=['POST'])
def model4_prediction():
    data = request.json
    response = run_model_script('model4', data)
    return jsonify(response)

@app.route('/model5-prediction', methods=['POST'])
def model5_prediction():
    data = request.json
    response = run_model_script('model5', data)
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5012)

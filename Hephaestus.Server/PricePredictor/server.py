from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import subprocess
import json
import re

app = Flask(__name__)
CORS(app)

def clean_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def get_last_json_line(text):
    # Pobierz ostatnią linię, która wygląda jak JSON
    lines = text.strip().split('\n')
    for line in reversed(lines):
        line = line.strip()
        if line.startswith('{') and line.endswith('}'):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    raise ValueError("No valid JSON found in output")

def run_model_script(model_name, data):
    script_path = f"./PricePredictor/{model_name}_prediction.py"
    input_data = json.dumps(data)
    result = subprocess.run(['python', script_path, input_data], capture_output=True, text=True, encoding='utf-8')
    # Logowanie wyników dla debugowania
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    
    # Sprawdzanie czy skrypt zwrócił jakikolwiek błąd
    if result.returncode != 0:
        return {"error": "Script returned non-zero exit code", "stderr": result.stderr}
    #cleaned_stdout = clean_ansi_escape_sequences(result.stdout)
    #print("cleaned_stdout:", cleaned_stdout)
    try:
        # Pobranie ostatniej linii JSON z wyniku skryptu
        output = get_last_json_line(result.stdout)
        print(output)
    except ValueError as e:
        return {"error": "JSON decode error", "message": str(e), "stdout": result.stdout}

    #output = json.loads(result.stdout)
    return output

@app.route('/model1-prediction', methods=['POST'])
def model1_prediction():
    data = request.json['dataframe_split']
    response = run_model_script('model1', data)
    return jsonify(response)

@app.route('/model2-prediction', methods=['POST'])
def model2_prediction():
    data = request.json['dataframe_split']
    response = run_model_script('model2', data)
    return jsonify(response)

@app.route('/model3-prediction', methods=['POST'])
def model3_prediction():
    data = request.json['dataframe_split']
    response = run_model_script('model3', data)
    return jsonify(response)

@app.route('/model4-prediction', methods=['POST'])
def model4_prediction():
    data = request.json['dataframe_split']
    response = run_model_script('model4', data)
    return jsonify(response)

@app.route('/model5-prediction', methods=['POST'])
def model5_prediction():
    data = request.json['dataframe_split']
    response = run_model_script('model5', data)
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5012)

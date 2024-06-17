import sys
import json
import mlflow
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import tensorflow as tf

# ----- Przygotowanie danych -----

input_data = json.loads(sys.argv[1])
columns = input_data['columns']
data = input_data['data']

example_data = pd.DataFrame(data, columns=columns)

# Konwersja kolumny DATE i POTENTIAL_DATE na obiekty datetime
example_data['DATE'] = pd.to_datetime(example_data['DATE'])
example_data['POTENTIAL_DATE'] = pd.to_datetime(example_data['POTENTIAL_DATE'])

# Dodanie cechy - liczba dni między DATE a POTENTIAL_DATE
example_data['DAYS_BETWEEN'] = (example_data['POTENTIAL_DATE'] - example_data['DATE']).dt.days

# Label Encoding dla kolumny FAILURE_TYPE (używając tych samych etykiet jak w treningu)

# Usuwanie oryginalnych kolumn DATE i POTENTIAL_DATE
example_data = example_data.drop(columns=['DATE', 'POTENTIAL_DATE'])

# Skalowanie danych (używając tego samego skalera jak w treningu)
scaler = StandardScaler()
example_data_scaled = scaler.fit_transform(example_data)

# ----- Ładowanie modelu i wykonywanie przewidywania -----

mlflow.set_tracking_uri(uri="http://127.0.0.1:5000")

model_uri = 'runs:/9622ccab7dae41a2bf559d5d849b9913/model1'
loaded_model = mlflow.pyfunc.load_model(model_uri)

predicted_price = loaded_model.predict(example_data_scaled)

print(json.dumps({"predicted_price": predicted_price[0]}))

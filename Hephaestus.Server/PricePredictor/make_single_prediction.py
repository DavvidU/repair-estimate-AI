import mlflow
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import tensorflow as tf

# ----- Przygotowanie przykładowych danych -----

# Przykładowa awaria
example_data = pd.DataFrame({
    'FAILURE_TYPE': ['Low'],
    'DATE': ['2024-02-02'],
    'POTENTIAL_DATE': ['2027-02-11']
})

# Konwersja kolumny DATE i POTENTIAL_DATE na obiekty datetime
example_data['DATE'] = pd.to_datetime(example_data['DATE'])
example_data['POTENTIAL_DATE'] = pd.to_datetime(example_data['POTENTIAL_DATE'])

# Dodanie cechy - liczba dni między DATE a POTENTIAL_DATE
example_data['DAYS_BETWEEN'] = (example_data['POTENTIAL_DATE'] - example_data['DATE']).dt.days

# Label Encoding dla kolumny FAILURE_TYPE (używając tych samych etykiet jak w treningu)
label_encoder = LabelEncoder()
label_encoder.fit(['Low', 'Mild', 'High', 'Critical'])
example_data['FAILURE_TYPE'] = label_encoder.transform(example_data['FAILURE_TYPE'])

# Usuwanie oryginalnych kolumn DATE i POTENTIAL_DATE
example_data = example_data.drop(columns=['DATE', 'POTENTIAL_DATE'])

# Skalowanie danych (używając tego samego skalera jak w treningu)
scaler = StandardScaler()
example_data_scaled = scaler.fit_transform(example_data)

# ----- Ładowanie modelu i wykonywanie przewidywania -----

mlflow.set_tracking_uri(uri="http://127.0.0.1:5000")

model_uri = 'runs:/361edb364e874634a9a0608a2318952a/model1'
loaded_model = mlflow.pyfunc.load_model(model_uri)

predicted_price = loaded_model.predict(example_data_scaled)

print(f"Przewidywana cena naprawy: {predicted_price[0]}")

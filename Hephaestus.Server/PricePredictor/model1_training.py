# Przygotowanie danych
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
# Trenowanie modeli
import tensorflow as tf
from tensorflow import keras
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import Dense
from sklearn.metrics import accuracy_score, precision_score, f1_score
import mlflow
import mlflow.tensorflow

# ----- Przygotowanie danych -----

data = pd.read_csv('./PricePredictor/data/cleansed_data.csv')

# Konwersja kolumny DATE i POTENTIAL_DATE na obiekty datetime
data['DATE'] = pd.to_datetime(data['DATE'])
data['POTENTIAL_DATE'] = pd.to_datetime(data['POTENTIAL_DATE'])

# Dodanie cechy - liczba dni między DATE a POTENTIAL_DATE
data['DAYS_BETWEEN'] = (data['POTENTIAL_DATE'] - data['DATE']).dt.days

# Label Encoding dla kolumny FAILURE_TYPE
label_encoder = LabelEncoder()
data['FAILURE_TYPE'] = label_encoder.fit_transform(data['FAILURE_TYPE'])

# Usuwanie oryginalnych kolumn DATE i POTENTIAL_DATE
data = data.drop(columns=['DATE', 'POTENTIAL_DATE'])

# X - cechy; Y - etykiety
X = data.drop(columns=['POTENTIAL_PRICE'])
y = data['POTENTIAL_PRICE']

# Skalowanie danych
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Podział danych na zestawy treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ----- Sprawdzenie danych ---------------
print(data.head())

# ----- Definiowanie i trenowanie modeli -----

# Dwie warstwy ukryte po 64, funkcja aktywacji - relu

def create_model():
    model = Sequential([
        Dense(256, activation='relu'),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    return model

mlflow.set_tracking_uri(uri="http://127.0.0.1:5000")
mlflow.set_experiment("Failure repair costs predictions")

model = create_model()
model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=0) # trening, mini-batch gradient descent

# Dokonywanie predykcji

y_pred = model.predict(X_test)
y_pred = y_pred.round().astype(int).flatten()

# Ocena modelu

accuracy = accuracy_score(y_test, y_pred)
precision_macro = precision_score(y_test, y_pred, average='macro', zero_division=1)
precision_micro = precision_score(y_test, y_pred, average='micro', zero_division=1)
precision_weighted = precision_score(y_test, y_pred, average='weighted', zero_division=1)

f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=1)
f1_micro = f1_score(y_test, y_pred, average='micro', zero_division=1)
f1_weighted = f1_score(y_test, y_pred, average='weighted', zero_division=1)

# Logowanie modelu i metryk w MLFlow

#signature = mlflow.models.signature.infer_signature(X_train, model.predict(X_train))
with mlflow.start_run():
    mlflow.tensorflow.log_model(model, "model1")
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision_macro", precision_macro)
    mlflow.log_metric("precision_micro", precision_micro)
    mlflow.log_metric("precision_weighted", precision_weighted)
    mlflow.log_metric("f1_macro", f1_macro)
    mlflow.log_metric("f1_micro", f1_micro)
    mlflow.log_metric("f1_weighted", f1_weighted)
import pandas as pd
import numpy as np
import random
import string
from datetime import datetime

data = pd.read_csv('./PricePredictor/data/failures_data.csv')

def generate_random_name(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_random_status():
    statuses = ['NEW', 'IN_PROGRESS', 'FINISHED', 'UNREPAIRABLE']
    return random.choice(statuses)

# Ustalanie zakresu dat dla DATE i POTENTIAL_DATE
min_date = datetime.strptime(data['DATE'].min(), "%Y-%m-%d")
max_date = datetime.strptime(data['DATE'].max(), "%Y-%m-%d")
min_potential_date = datetime.strptime(data['POTENTIAL_DATE'].min(), "%Y-%m-%d")
max_potential_date = datetime.strptime(data['POTENTIAL_DATE'].max(), "%Y-%m-%d")

# Obliczanie średniej i odchylenia standardowego dla POTENTIAL_PRICE dla każdego FAILURE_TYPE
price_stats = data.groupby('FAILURE_TYPE')['POTENTIAL_PRICE'].agg(['mean', 'std']).reset_index()

new_data = []

for _ in range(100):
    failure_type = random.choice(data['FAILURE_TYPE'].unique())
    
    # Pobieranie średniej i odchylenia standardowego dla wybranego FAILURE_TYPE
    stats = price_stats[price_stats['FAILURE_TYPE'] == failure_type]
    mean_price = stats['mean'].values[0]
    std_price = stats['std'].values[0]
    
    name = generate_random_name()
    date = min_date + (max_date - min_date) * random.random()
    potential_price = max(0, np.random.normal(mean_price, std_price))
    potential_price = round(potential_price)
    potential_date = min_potential_date + (max_potential_date - min_potential_date) * random.random()
    status = generate_random_status()
    
    new_data.append([failure_type, name, date.strftime("%Y-%m-%d"), potential_price, potential_date.strftime("%Y-%m-%d"), status])

# Konwersja nowych danych do DataFrame
new_data_df = pd.DataFrame(new_data, columns=['FAILURE_TYPE', 'NAME', 'DATE', 'POTENTIAL_PRICE', 'POTENTIAL_DATE', 'STATUS'])

# Połączenie oryginalnych i nowych danych
augmented_data = pd.concat([data, new_data_df], ignore_index=True)

# Zapisanie połączonych danych do pliku CSV
augmented_data.to_csv('./PricePredictor/data/augmented_data.csv', index=False)

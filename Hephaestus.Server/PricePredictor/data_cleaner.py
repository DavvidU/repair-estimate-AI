import pandas as pd

data = pd.read_csv('./PricePredictor/data/augmented_data.csv')

# Usunięcie kolumn NAME, DATE, POTENTIAL_DATE oraz STATUS
cleansed_data = data.drop(columns=['NAME', 'STATUS'])

cleansed_data.to_csv('./PricePredictor/data/cleansed_data.csv', index=False)

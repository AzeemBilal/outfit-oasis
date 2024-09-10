import pandas as pd
import numpy as np
import joblib

loaded_pipeline = joblib.load('model.pkl')

def predict_top_n_classes_loaded(price, category, n=3):
    single_record = pd.DataFrame([[price, category]], columns=['price', 'category'])
    probabilities = loaded_pipeline.predict_proba(single_record)
    top_n_indices = np.argsort(probabilities[0])[-n:][::-1]
    top_n_classes = [loaded_pipeline.classes_[i] for i in top_n_indices]
    top_n_probabilities = probabilities[0][top_n_indices]
    return list(zip(top_n_classes, top_n_probabilities))

min_price = 500 
max_price = 2500 
category = 'Pant'  

price = (min_price + max_price) / 2
top_n_results = predict_top_n_classes_loaded(price, category, n=5)
print("The top 5 predicted stores for the product are: ")
for i in top_n_results:
    print (i)

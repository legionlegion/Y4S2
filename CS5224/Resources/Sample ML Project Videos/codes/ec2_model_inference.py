"""
ec2 model inference
"""

import sys
import pandas as pd
from joblib import load
from sklearn.preprocessing import StandardScaler

def scale_data(X):
    scaler = StandardScaler()
    X_numerical = X.select_dtypes(include=["int", "float"])
    X_categorical = X.select_dtypes(exclude=["int", "float"])
    X_scaled = scaler.fit_transform(X_numerical)
    X_scaled = pd.DataFrame(X_scaled, columns = X_numerical.columns)
    X_scaled = pd.concat([X_scaled, X_categorical],axis=1)
    
    return X_scaled

model = load(sys.argv[1])
input_file = sys.argv[2]
output_file = sys.argv[3]

# preprocess
df = pd.read_csv(input_file)

df.drop(columns=["ID", "No_Patient"], inplace=True)
df_scaled = scale_data(df)
df_scaled = pd.get_dummies(df_scaled, columns=["Gender"], drop_first=True, dtype=int)

# predict
pred = model.predict(df_scaled)
pred = pd.DataFrame(pred, columns=['CLASS'])
pred.to_csv(output_file)

print(f"Processed {input_file} -> {output_file}")

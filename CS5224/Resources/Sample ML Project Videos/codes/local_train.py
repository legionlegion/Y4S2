"""
locally train ML model
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from joblib import dump, load

def scale_data(X):
    scaler = StandardScaler()
    X_numerical = X.select_dtypes(include=["int", "float"])
    X_categorical = X.select_dtypes(exclude=["int", "float"])
    X_scaled = scaler.fit_transform(X_numerical)
    X_scaled = pd.DataFrame(X_scaled, columns = X_numerical.columns)
    X_scaled = pd.concat([X_scaled, X_categorical],axis=1)
    
    return X_scaled

# =====================
# 1. Preprocessing
# =====================
data = pd.read_csv("diabetes.csv")

# Get features and target
X = data.drop(columns=["ID", "No_Patient", "CLASS"])
y = data["CLASS"]

# Scale numerical features
X_scaled = scale_data(X)

# Encode categorical features
X_scaled = pd.get_dummies(X_scaled, columns=["Gender"], drop_first=True, dtype=int)

# =====================
# 2. Train/test split
# =====================
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# =====================
# 3. Train MLP
# =====================
mlp = MLPClassifier(
    hidden_layer_sizes=(128, 64),
    activation="relu",
    solver="lbfgs",
    alpha=1e-4,
    learning_rate="adaptive",
    max_iter=1000,
    random_state=42
)

mlp.fit(X_train, y_train)

# =====================
# 4. Evaluation
# =====================
y_pred = mlp.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred))

# =====================
# 5. Save Model
# =====================
dump(mlp, 'model.joblib')
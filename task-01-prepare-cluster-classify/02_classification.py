# 02_classification.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# === 1. Load data hasil cluster ===
df = pd.read_csv("cluster_result.csv")

# === 2. Split features dan target ===
X = df[['EVI', 'NDVI', 'SAVI', 'NDWI', 'MNDWI', 'VCI']]
y = df['cluster']

# === 3. Split train-test ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# === 4. Train model klasifikasi ===
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# === 5. Evaluasi ===
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Akurasi model:", round(acc, 3))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

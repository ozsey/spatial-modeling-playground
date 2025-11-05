# 01_clustering.py
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# === 1. Load data ===
df = pd.read_csv("data_combined.csv")

# === 2. Normalisasi data ===
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# === 3. Tentukan K terbaik (Elbow Method) ===
inertias = []
K_range = range(2, 10)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

plt.plot(K_range, inertias, 'bo-')
plt.xlabel('Jumlah Cluster (k)')
plt.ylabel('Inertia')
plt.title('Metode Elbow untuk Menentukan k Terbaik')
plt.show()

# === 4. Pilih k terbaik (misal hasilnya 3, sesuaikan manual) ===
best_k = 3
model = KMeans(n_clusters=best_k, random_state=42)
df["cluster"] = model.fit_predict(X_scaled)

# === 5. Simpan hasil ===
df.to_csv("cluster_result.csv", index=False)
print("cluster_result.csv berhasil dibuat dengan", best_k, "cluster")

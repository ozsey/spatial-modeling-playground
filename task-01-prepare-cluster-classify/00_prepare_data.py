# 00_prepare_data.py
import rasterio
from rasterio.enums import Resampling
import numpy as np
import pandas as pd
import os

# === 1. Fungsi untuk membaca & resample band ke resolusi referensi ===
def read_and_resample(path, ref_profile):
    with rasterio.open(path) as src:
        if (src.height, src.width) != (ref_profile["height"], ref_profile["width"]):
            # Resample
            data = src.read(
                out_shape=(1, ref_profile["height"], ref_profile["width"]),
                resampling=Resampling.bilinear
            )[0]
        else:
            data = src.read(1)
    return data.astype("float32")

# === 2. Baca semua band ===
folder = "data"
b2_path = os.path.join(folder, "b2.tif")  # referensi 10m
with rasterio.open(b2_path) as ref:
    ref_profile = ref.profile

bands = {
    "BLUE": read_and_resample(os.path.join(folder, "b2.tif"), ref_profile),
    "GREEN": read_and_resample(os.path.join(folder, "b3.tif"), ref_profile),
    "RED": read_and_resample(os.path.join(folder, "b4.tif"), ref_profile),
    "RE": read_and_resample(os.path.join(folder, "b5.tif"), ref_profile),
    "NIR": read_and_resample(os.path.join(folder, "b8.tif"), ref_profile),
    "SWIR": read_and_resample(os.path.join(folder, "b11.tif"), ref_profile),
}

# === 3. Hitung indeks spektral ===
np.seterr(divide='ignore', invalid='ignore')

NDVI = (bands["NIR"] - bands["RED"]) / (bands["NIR"] + bands["RED"])
EVI = 2.5 * (bands["NIR"] - bands["RED"]) / (bands["NIR"] + 6 * bands["RED"] - 7.5 * bands["BLUE"] + 1)
SAVI = ((bands["NIR"] - bands["RED"]) / (bands["NIR"] + bands["RED"] + 0.5)) * 1.5
NDWI = (bands["GREEN"] - bands["NIR"]) / (bands["GREEN"] + bands["NIR"])
MNDWI = (bands["GREEN"] - bands["SWIR"]) / (bands["GREEN"] + bands["SWIR"])
VCI = (NDVI - np.nanmin(NDVI)) / (np.nanmax(NDVI) - np.nanmin(NDVI))

# === 4. Gabungkan ke DataFrame ===
df = pd.DataFrame({
    'EVI': EVI.flatten(),
    'NDVI': NDVI.flatten(),
    'SAVI': SAVI.flatten(),
    'NDWI': NDWI.flatten(),
    'MNDWI': MNDWI.flatten(),
    'VCI': VCI.flatten()
}).dropna()

# === 5. Simpan hasil gabungan ===
df.to_csv("data_combined.csv", index=False)
print("data_combined.csv berhasil dibuat, jumlah data:", len(df))

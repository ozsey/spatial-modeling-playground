setwd("/home/hose/Documents/PERMODELAN-SPESIAL/DATA/Latihan5")

# Instal dan muat package yang dibutuhkan
install.packages(c("sf", "sp", "fields", "ggplot2"))

library(sf)
library(sp)
library(fields)
library(ggplot2)

# Membaca data curah hujan dan shapefile Boyolali
hujan <- read.csv("/home/hose/Documents/PERMODELAN-SPESIAL/DATA/Latihan5/precipitasi2.csv", header = TRUE)
boyolali <- st_read("/home/hose/Documents/PERMODELAN-SPESIAL/DATA/Latihan5/boyolali3.shp")

# Menentukan koordinat titik curah hujan
coordinates(hujan) <- ~lon + lat
proj4string(hujan) <- CRS("+proj=longlat +datum=WGS84")

# Membuat grid untuk prediksi
grd <- as.data.frame(spsample(as_Spatial(boyolali), type = "regular", n = 10000))
names(grd) <- c("lon", "lat")

# Membuat model Thin Plate Spline (TPS)
tps_model <- Tps(coordinates(hujan), hujan$Dec)

# Prediksi nilai curah hujan pada grid
tps_pred <- predict(tps_model, grd)

# Menggabungkan hasil prediksi menjadi data frame
tps_df <- data.frame(
  lon = grd$lon,
  lat = grd$lat,
  var1.pred = tps_pred
)

# Visualisasi hasil interpolasi TPS
ggplot() +
  geom_tile(data = tps_df, aes(x = lon, y = lat, fill = round(var1.pred, 0)), alpha = 0.9) +
  scale_fill_gradient(low = "green", high = "red") +
  geom_sf(data = boyolali, fill = NA, color = "black", linewidth = 0.6) +
  geom_point(data = as.data.frame(hujan), aes(x = lon, y = lat),
             shape = 21, colour = "blue", fill = "yellow", size = 2.5) +
  labs(
    fill = "Curah Hujan (mm)",
    title = "Interpolasi Thin Plate Spline (TPS) - Curah Hujan Boyolali"
  ) +
  theme_minimal()

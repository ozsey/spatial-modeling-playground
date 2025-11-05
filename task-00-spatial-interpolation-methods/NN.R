setwd("/home/hose/Documents/PERMODELAN-SPESIAL/DATA/Latihan5")

# Instal dan muat package yang dibutuhkan
install.packages(c("sf", "sp", "gstat", "raster", "ggplot2"))

library(sf)
library(sp)
library(gstat)
library(raster)
library(ggplot2)

# Membaca data curah hujan dan shapefile Boyolali
hujan <- read.csv("/home/hose/Documents/PERMODELAN-SPESIAL/DATA/Latihan5/precipitasi2.csv", header = TRUE)
boyolali <- st_read("/home/hose/Documents/PERMODELAN-SPESIAL/DATA/Latihan5/boyolali3.shp")

# Menentukan koordinat titik curah hujan
coordinates(hujan) <- ~lon + lat
proj4string(hujan) <- CRS("+proj=longlat +datum=WGS84")

# Membuat grid untuk interpolasi
grd <- as.data.frame(spsample(as_Spatial(boyolali), type = "regular", n = 10000))
names(grd) <- c("lon", "lat")
coordinates(grd) <- ~lon + lat
gridded(grd) <- TRUE
proj4string(grd) <- CRS("+proj=longlat +datum=WGS84")

# Membuat model Nearest Neighbor (NN)
nn_model <- gstat(formula = Dec ~ 1, locations = hujan, nmax = 1, set = list(idp = 0))

# Melakukan prediksi dengan NN
nn_result <- predict(nn_model, grd)
nn_df <- as.data.frame(nn_result)
names(nn_df)[1:2] <- c("lon", "lat")

# Visualisasi hasil interpolasi
ggplot() +
  geom_tile(data = nn_df, aes(x = lon, y = lat, fill = round(var1.pred, 0)), alpha = 0.9) +
  scale_fill_gradient(low = "green", high = "red") +
  geom_sf(data = boyolali, fill = NA, color = "black", linewidth = 0.6) +
  geom_point(data = as.data.frame(hujan), aes(x = lon, y = lat),
             shape = 21, colour = "blue", fill = "yellow", size = 2.5) +
  labs(fill = "Curah Hujan (mm)",
       title = "Interpolasi Nearest Neighbor (NN) - Curah Hujan Boyolali") +
  theme_minimal()


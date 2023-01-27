import csv
import random
from datetime import datetime, timedelta

# Set the geographic coordinate boundaries for California
lat_min = 32.53
lat_max = 42.01
lon_min = -124.48
lon_max = -114.13

# Set the range for temperature and conductivity values
temp_min = 18
temp_max = 21
cond_min = 160
cond_max = 180

# Open the .csv file and write the header
with open('well_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Well", "Latitude", "Longitude", "DateTime", "Temperature (C)", "Conductivity (microS/cm)"])

# Set the starting date and time
start_date = datetime(2022,1,1,12,0,0)

# Generate random well location in CA
lat = round(random.uniform(lat_min, lat_max), 4)
lon = round(random.uniform(lon_min, lon_max), 4)

# Write the data for "Well 1"
# 48 iterations equiv to 2 hours data w/ 5 min incremenet
for i in range(48):
    date_time = start_date + timedelta(minutes=5*i)
    temp = round(random.uniform(temp_min, temp_max), 2)
    conductivity = round(random.uniform(cond_min, cond_max), 2)
    with open('well_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Well 1", lat, lon, date_time, temp, conductivity])
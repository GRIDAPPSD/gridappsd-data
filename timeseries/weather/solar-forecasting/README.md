
Make sure that InfluxDB Docker container is up and running.

# Steps to import weather data:

1. Build InfluxDB import file

   `python3 process_weather_data.py`

2. Copy import file inside InfluxDB Docker container

   `docker cp weather_import_file.txt influxdb:/.`

3. Import data in InfluxDB

   `docker exec -t influxdb influx -import -path weather_import_file.txt -precision s`
   
# To use custom weather data:
1. Get the weather data in a csv file.
2. Make sure the headers and date format is same as in GHI_DHI_Temp_Wind_20130101_english_units_clean.csv.
3. Change csv file name in process_weather_data.py on line number 9.


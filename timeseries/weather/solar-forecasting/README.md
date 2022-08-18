
Make sure influxdb is loaded.

To use custom weather data file, change file name in process_weather_data.py on line number 9. 

Steps:

1. Build InfluxDB import file
   
   `python3 process_weather_data.py`

2. Import data in InfluxDB

   `docker exec -t influxdb influx -import -path weather_import_file.txt -precision s`


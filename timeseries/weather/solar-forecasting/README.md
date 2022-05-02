# Weather data

Weather data available in the GridAPPS-D platform is under timeseries/weather/solar-forecasting/GHI_DHI_Temp_Wind_20130101_english_units_clean.csv. The data is uploaded to the timeseries datastore (influxdb) under its own docker container.

### Pre-requisites:

- Make sure influxdb container is up and running

    `docker ps -f "name=influxdb"`

- Install python requirements

    `cd gridappsd-data/timeseries/weather/solar-forecasting/`
  
    `pip3 install -r requirements.txt`

### Steps to upload data:

1. Clone this repository

    `git clone https://gridappsd/gridappsd-data.git`

2. Create bulk load file

    `cd gridappsd-data/timeseries/weather/solar-forecasting/`

    `python3 build_bulk_load_file.py`

3. Copy bulk load file inside timeseries datastore container

    `docker cp ghi_dhi_bulkload.txt influxdb:/`

4. Uplaod data 

    `docker exec -t influxdb influx -import -path=ghi_dhi_bulkload.txt -precision ms`

## Custom data 
To upload user defined custom data, 

1. Make a csv file using the same format as timeseries/weather/solar-forecasting/GHI_DHI_Temp_Wind_20130101_english_units_clean.csv

2. Edit below line in timeseries/weather/solar-forecasting/build_bulk_load_file.py

    From: 
      `raw_input_weather_file = 'GHI_DHI_Temp_Wind_20130101_english_units_clean.csv'`

    To: `raw_input_weather_file = '<custom_data_file_name>.csv'`

3. Follow the steps above to upload data 


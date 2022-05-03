
# Load Profile Data

Load profile data available in the GridAPPS-D platform is in timeseries/loadprofile/ieeezipload.player file. The data is uploaded to the timeseries datastore (influxdb).

### Pre-requisites:

- Make sure influxdb container is up and running

    `docker ps -f "name=influxdb"`
    
- Python3


### Steps to upload data:

1. Clone this repository

    `git clone https://gridappsd/gridappsd-data.git`

2. Create bulk load file

    `cd gridappsd-data/timeseries/loadprofile/`

    `python3 loadprofile_measurement_bulk.py`

3. Copy bulk load file inside timeseries datastore container

    `docker cp loadprofile_measurement_out.txt influxdb:/`

4. Uplaod data 

    `docker exec -t influxdb influx -import -path=loadprofile_measurement_out.txt -precision s`

## Custom data 
To upload custom loadprofile data, execute following steps. This will replace existing loadprofile data.

1. Make a player file using the same format as timeseries/loadprofile/ieeezipload.player

2. Edit below line in timeseries//loadprofile/loadprofile_measurement_bulk.py

    From: `raw_input_file = "ieeezipload.player"`

    To: `raw_input_file = '<custom_data_file_name>.player'`

3. Follow the steps above to upload data

FROM influxdb:1.8 AS influxdbbuild

ARG TIMESTAMP
RUN echo $TIMESTAMP > /dockerbuildversion.txt

COPY ./timeseries /tmp/timeseries
RUN apt-get update \
    && apt-get install -y \
       python3 \
       python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives/*  \
    && pip3 install -r /tmp/timeseries/weather/solar-forecasting/requirements.txt  \
    && cd /tmp/timeseries/weather/solar-forecasting \
    && python3 process_weather_data.py \
    && cd /tmp/timeseries/loadprofiles \
    && python3 loadprofile_measurement_bulk.py 

FROM influxdb:1.8 

COPY --from=influxdbbuild /tmp/timeseries/weather/solar-forecasting/weather_import_file.txt /tmp/weather_import_file.txt
COPY --from=influxdbbuild /tmp/timeseries/loadprofiles/loadprofile_measurement_out.txt /tmp/loadprofile_measurement_out.txt
COPY --from=influxdbbuild /dockerbuildversion.txt /dockerbuildversion.txt
COPY ./influxdb.conf /etc/influxdb/influxdb.conf

ENV INFLUXDB_DB=proven
EXPOSE 8086
RUN mkdir -p /data/influxdb \
    && chown influxdb:influxdb /data/influxdb

FROM influxdb:latest AS influxdbbuild

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
    && python3 build_bulk_load_file.py  \
    && egrep -v "DATE=\"[6789]" ghi_dhi_bulkload.txt > ghi_dhi_bulkload.txt.tmp \
    && mv ghi_dhi_bulkload.txt.tmp ghi_dhi_bulkload.txt \
    && python3 build_bulk_load_file_modified.py  \
    && cat ghi_dhi_bulkload_modified.txt >> ghi_dhi_bulkload.txt

FROM influxdb:latest 

COPY --from=influxdbbuild /tmp/timeseries/weather/solar-forecasting/ghi_dhi_bulkload.txt /tmp/ghi_dhi_bulkload.txt
COPY --from=influxdbbuild /dockerbuildversion.txt /dockerbuildversion.txt
COPY ./influxdb.conf /etc/influxdb/influxdb.conf

ENV INFLUXDB_DB=proven
EXPOSE 8086
RUN mkdir -p /data/influxdb \
    && chown influxdb:influxdb /data/influxdb

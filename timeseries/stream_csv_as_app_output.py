"""
This script reads all the csv files in the given folder and 
publishes the data as an application output. The published data gets
stored in the timeseries datastore as well.

"""

import argparse
import csv
import logging
import os

from datetime import datetime
from gridappsd import GridAPPSD
from gridappsd import topics

_log = logging.getLogger(__name__)

def _main():
    _log.debug("Starting application")
    parser = argparse.ArgumentParser()
    parser.add_argument("app_name",
                        help="Application name")
    parser.add_argument("folder_path",
                        help="Folder path where files are located")
    parser.add_argument("--simulation_id",
                        help="Simulation id to use for responses on the message bus.",
                        default=None)
    
    opts = parser.parse_args()
    
    gapps = GridAPPSD()
    topic = topics.application_output_topic(opts.app_name, opts.simulation_id)
    
    for file in os.listdir(opts.folder_path):
        if file.endswith(".csv"):
            data = {}
            data['timestamp'] = int(datetime.now().timestamp())
            data['datatype'] = file.split('.')[0]
            if opts.simulation_id is not None:
                data['simulation_id'] = str(opts.simulation_id)
                data['tags'] = ["simulation_id"]
            data['message'] = []

            file_path = opts.folder_path + '/' + file
            with open(file_path, newline='', encoding="utf-8-sig") as csvfile:
                reader = csv.DictReader(csvfile, skipinitialspace=True)
                for row in reader:
                    data['message'].append(row)

            print(data)
            print('\n\n')
            gapps.send(topic,data)

   
if __name__ == "__main__":
    _main()

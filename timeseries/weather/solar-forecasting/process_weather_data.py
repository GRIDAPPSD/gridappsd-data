'''
Created on Sep 21, 2018
@author: ericstephan
'''
import time, os
import datetime as dt 
import pytz

raw_input_weather_file = 'GHI_DHI_Temp_Wind_20130101_english_units_clean.csv'
bulk_load_output_file = "weather_import_file.txt"
measurement = "weather_default"
database = "proven"
daylight_savings_time = True

override_date_dict =    {
  "newval": 2022,
  "datetype": "Y",
  "delimiter": "/"
}

tz = pytz.timezone('UTC')


def override_date(override_date_dict):
    return override_date_dict

def utc_offset(daylight):                     
    epoch_onehour = 3600
    val = epoch_onehour
    if (daylight):
        val = 3600 * 6
    else:
        val = 3600 * 7
    return val

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def process_value(s):
    if (is_number(s)):
        return s
    else:
        s = "\"" + s + "\""
    return s 
        
def strip_extra_chars(s):
        s = s.rstrip(" ")
        s = s.rstrip("\t")
        s = s.rstrip("\m")
        s = s.rstrip("\n")
        s = s.rstrip("\r")
        return s

def create_import_header_lines(database):
    s = "# DML \n"
    s = s + "# CONTEXT-DATABASE: proven \n"
    s = s + "# CONTEXT-RETENTION-POLICY: autogen \n\n"
    #s = "# DROP DATABASE " + database + "\n"
    #s = s + "# CREATE DATABASE " + database + "\n"
    #s = s + "# DML\n"
    #s = s + "# CONTEXT-DATABASE: " + database + "\n"
    #s = s + "# CONTEXT-RETENTION-POLICY: autogen \n"
    #s = s + "USE proven\n\n"
    return s



def add_tags(measurement_name):
        measurement = measurement_name
        place = "Solar\ Radiation\ Research\ Laboratory"
        lat = "39.74\ N"
        long = "105.18\ W"
        tags = "place=\"" + place + "\",lat=\"" + lat + "\",long=\"" + long + "\" "
        return tags
        
        

count = 0;
title_tokens = ""
title_columns = 0
with open(raw_input_weather_file) as fin:
    for line in fin:
        line = strip_extra_chars(line)
        count = count + 1
        if (count == 2):
            title_tokens = line.split(",") 

            print(line)
            title_columns = len(title_tokens)
            break
        else:
            pass

count = 0
while (count < title_columns):
    buff  = title_tokens[count]
    buff = buff.replace(" ", "\\ ")
    title_tokens[count] = buff
    count = count + 1;

count = 0
data_columns = 0
data_tokens = ""
#fo = open(bulk_load_output_file,'w')
#fo.write(create_import_header_lines(database))

with open(bulk_load_output_file,'w') as file_out:
    file_out.write(create_import_header_lines(database))
    with open(raw_input_weather_file) as fin:
        for line in fin:
            line = strip_extra_chars(line)
            count = count + 1
            if (count > 2):
                data_tokens = line.split(",") 
                data_columns = len(data_tokens)
                if ((data_columns) != title_columns) :
                    print ("ERROR:  " + line)
                    print ("ERROR: " + str(data_columns) + " " + str(title_columns) + "\n")
                    break
                else:
                    column_counter = 0
                    newline = ""
                    while (column_counter < title_columns):
                        if (column_counter == 0) :
                            newline = title_tokens[column_counter] + "=" + process_value(data_tokens[column_counter]) 
                        else: 
                            newline = newline + "," + title_tokens[column_counter] + "=" + process_value(data_tokens[column_counter])
                        column_counter = column_counter + 1;

                        d=data_tokens[0] + " " + data_tokens[1] 
                        p='%m/%d/%y %H:%M'
                    
                    d_datetime = dt.datetime.strptime(d,p)
                    d_datetime = d_datetime.replace(year=2013)
                    epoch = int(tz.localize(d_datetime).timestamp())
                    file_out.write( measurement + "," + add_tags(measurement) + " " + newline + " " + str(epoch) + "\n" )
    #fo.close()
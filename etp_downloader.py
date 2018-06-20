#! /usr/bin/env python


import requests, logging, json
from http_calls import EdgeGridHttpCaller

from akamai.edgegrid import EdgeGridAuth
import os
import datetime
from datetime import timedelta
import math
import argparse
from logging.handlers import RotatingFileHandler
import time
from flatten_json import flatten_json
from pandas.io.json import json_normalize

session = requests.Session()

default_download_folder="./akamai-etp-reports"
script_name = "akamai-etp-to-splunk"

parser = argparse.ArgumentParser(description='Download reports from Akamai ETP')
parser.add_argument('-s','--server', help='Akamai ETP Servername', required=True)
parser.add_argument('-r','--read_file', help='Read this file instead of making a web request (for DEBUG)', required=False)
parser.add_argument('-l','--log_file', help='Log to file instead of STDERR', required=False)
parser.add_argument('-D','--debug', help='Debug', action="store_true", required=False)
parser.add_argument('-d','--download_folder', help='Destination folder for CSVs - default to "' + default_download_folder + '"', required=False, default=default_download_folder)
args = parser.parse_args()

# Logging
if args.debug:
    log_level = logging.DEBUG
else:
    log_level = logging.INFO

logger = logging.getLogger()
logger.level = log_level


if args.log_file:
    rotationHandler = RotatingFileHandler(args.log_file, mode='a', maxBytes=5*1024*1024, backupCount=1)
    rotationHandler.setLevel(log_level)
    rotationHandler.setFormatter(logging.Formatter('%(asctime)s - ' + script_name + ' - %(levelname)s - %(message)s'))
    logger.addHandler(rotationHandler)
else:
    logger.addHandler(logging.StreamHandler())

# Log the command line options
logger.debug(args)

def create_caller():
    # Set the config options
    session.auth = EdgeGridAuth(
        client_token=os.environ['ETP_CLIENT_TOKEN'].strip(),
        client_secret=os.environ['ETP_CLIENT_SECRET'].strip(),
        access_token=os.environ['ETP_ACCESS_TOKEN'].strip()
    )

    baseurl = '%s://%s/' % ('https', args.server.strip())
    httpCaller = EdgeGridHttpCaller(session, baseurl, args.debug)
    return httpCaller

def get_timestamp_of_previous_run():
    if(os.path.isdir(args.download_folder)):
        dirlist = os.listdir(args.download_folder)
        files = []
        for e in dirlist:
            path = os.path.join(args.download_folder, e)
            if not(os.path.isdir(path)) and path.endswith(".csv"):
                files.append(e)
        sorted_files = sorted(files)
        if(len(sorted_files) > 0):
            return sorted_files[len(sorted_files)-1].split('_')[1].split('.')[0]
    return get_default_start_time()

def get_default_start_time():
    dt = datetime.datetime.now() - timedelta(days=30)
    ts = int(math.floor((dt - datetime.datetime(1970, 1, 1)).total_seconds()))
    return ts

def fetch_threat_events_in_period(caller, configuration_id, start, end):
    events_result = None
    if not(args.read_file):
        events_result = caller.getResult('/etp-report/v1/configs/%s/threat-events/details?startTimeSec=%s&endTimeSec=%s' % (configuration_id, start, end))
    else:
        with open(args.read_file) as f:
            events_result = json.load(f)
    if(len(events_result) > 0 ):
        csv = convert_to_csv(events_result)
        saveCsvToFile(csv, end)

def saveCsvToFile(csv, timestamp):
    full_filename = os.path.join(args.download_folder, "etp_"+str(timestamp)+".csv")
    f = open(full_filename, 'w+')
    f.write(csv)


def convert_to_csv(etp_reports):
    header = ""
    header =  "policyName,confidenceId,categoryName,actionName,listName,siteName,description,"
    header += "confidenceName,listId,reason,trigger,siteId,"
    header += "policyId,detectionTime,detectionType,categoryId,actionId,configId,"
    header += "asname,type,response,asn,deviceName,domain,uuid,time,deviceId,dnsIp,clientIp,queryType,id,l7Protocol"

    rows = ""
    for r in etp_reports:
        flat = flatten_json(r)
        n = json_normalize(flat)

        dict = n.iloc[0].to_dict()
        row = dict['event_policyName'] + ","
        row += dict['event_confidenceId'] + ","
        row += dict['event_categoryName'] + ","
        row += dict['event_actionName'] + ","
        row += dict['event_listName'] + ","
        row += dict['event_siteName'] + ","
        row += dict['event_description'] + ","
        row += dict['event_confidenceName'] + ","
        row += dict['event_listId'] + ","
        row += dict['event_reason'] + ","
        row += dict['event_trigger'] + ","
        row += dict['event_siteId'] + ","
        row += dict['event_policyId'] + ","
        row += dict['event_detectionTime'] + ","
        row += dict['event_detectionType'] + ","
        row += dict['event_categoryId'] + ","
        row += dict['event_actionId'] + ","
        row += dict['configId'] + ","
        row += dict['query_resolved_0_asname'] + ","
        row += dict['query_resolved_0_type'] + ","
        row += dict['query_resolved_0_response'] + ","
        row += dict['query_resolved_0_asn'] + ","
        row += dict['query_deviceName'] + ","
        row += dict['query_domain'] + ","
        row += dict['query_uuid'] + ","
        row += dict['query_time'] + ","
        row += dict['query_deviceId'] + ","
        row += dict['query_dnsIp'] + ","
        row += dict['query_clientIp'] + ","
        row += dict['query_queryType'] + ","
        row += dict['id'] + ","
        row += dict['l7Protocol'] + ","
        rows = rows + "\n" + row

    return header + "\n" + rows

def get_configuration_id(caller):
    return caller.getResult('/etp-config/v1/configs')[0]



if __name__ == "__main__":
    caller = create_caller()
    configuration_id = get_configuration_id(caller)
    timestamp_previous_run = get_timestamp_of_previous_run()
    fetch_threat_events_in_period(caller, configuration_id, timestamp_previous_run, int(time.time()))
    exit(0)

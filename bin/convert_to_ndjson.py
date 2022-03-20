#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
file:    convert_to_ndjson.py
author:  rbw
version: 1.0-RC1
date:    Sun Mar 20 16:38:33 EDT 2022
purpose:
  Convert PiAware raw data, in JSON format, to NDJSON
  for ingestion into Elasticsearch
"""
import sys
import os
import time
import requests
import math
import json
import pprint as pp
from datetime import datetime


def convert_to_ndjson(pa_file):
    #print(pa_file)
    with open(pa_file) as fp:
        pa_data = json.load(fp)

    # convert timestamp to string
    #pp.pprint(pa_data)
    dt = datetime.fromtimestamp(pa_data['now'])
    dtx = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")
    #print(f'dtx: {dtx}')
    #print(f'dt: {dt}')

    # number of messages
    num_msgs = pa_data['messages']
    #print(f'num_msgs: {num_msgs}')

    # iterate over all aircraft records
    ac_count = 0
    for aircraft in pa_data['aircraft']:
        # add meta-parameters
        aircraft['now'] = dtx
        aircraft['num_msgs'] = num_msgs
        ac_count += 1
        #print(ac_count)
        #pp.pprint(aircraft)
        # print single line of NDJSON
        andj = json.dumps(aircraft)
        print(andj)


def convert_multiple_files(pa_file_or_dir):
    if os.path.isdir(pa_file_or_dir):
        dir_w_slash = pa_file_or_dir
        if pa_file_or_dir.endswith('/'):
            dir_w_slash = pa_file_or_dir
        else:
            dir_w_slash = pa_file_or_dir + os.sep
        # todo: handle nested directories
        file_list = os.listdir(pa_file_or_dir)
        for file in file_list:
            #print(f"file: {file}")
            path = dir_w_slash + file
            print(path)
            convert_to_ndjson(path)
    elif os.path.isfile(pa_file_or_dir):
        convert_to_ndjson(pa_file_or_dir)
    else:
        print(f'error: "{pa_file_or_dir}" is not a file or directory')

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 2:
        print(f"usage: {sys.argv[0]} piaware-file-or-directory")
    convert_multiple_files(sys.argv[1])
    sys.exit(0)
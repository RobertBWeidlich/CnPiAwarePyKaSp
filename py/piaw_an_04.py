#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file:   piaw_an_04.py
author: rbw
date:   Sat May  9 12:34:49 EDT 2020
purpose:
  Loop to periodically poll the PiAware
  Retrieve data from PiAware via REST interface
  preliminary analysis - track all hex number, figure out the different records
  Keep 2 lists:
    1. This - currently polled flights
    1. Legacy - all flights
    2. Tracking - only those new flights discovered after start.
         All flights in the This list not in Legacy and not in Tracking
         are added to this list
"""
import sys
import requests
import socket
import json
import time

URL = 'http://192.168.1.208:8080/data/aircraft.json'
POLL_PERIOD = 10     # seconds, must be integer > 0, should be 1,2,3,4,5,10,15,20,30, or 60
WAIT_OFFSET = 0.0
MAX_LOOP_COUNT = 10000000

hex_list_legacy = None  # aircraft we found at start - don't analyze
hex_list_tracking = []  # aircraft encountered after start

"""
Analyze data, which is expected to be in JSON format
"""
def analyze(json_data):
    global analyze_count
    global hex_list_legacy
    global hex_list_tracking
    data = json.loads(json_data)
    #print(data)
    now = data['now']
    #print("now: %f" % now)
    msg_count = data['messages']
    #print('msg_count: %d' % msg_count)
    aircraft_list = data['aircraft']

    hex_list = []
    for aircraft in aircraft_list:
        #print(aircraft)
        if 'hex' in aircraft:
            hex_list.append(aircraft['hex'])
    hex_list.sort()

    if not hex_list_legacy:
        hex_list_legacy = hex_list
        return

    # find new aircraft
    for hex_s in hex_list:
        if hex_s not in hex_list_legacy:
            print("new: %s" % hex_s)
            hex_list_legacy.append(hex_s)
            hex_list_tracking.append(hex_s)

    print("this    %d aircraft" % len(hex_list))
    print(hex_list)
    print("legacy  %d aircraft" % len(hex_list_legacy))
    print(hex_list_legacy)
    print("tracking: %d aircraft" % len(hex_list_tracking))
    print(hex_list_tracking)

    print('')


def main():
    loop_count = 0
    while True:
        loop_count += 1
        if loop_count > MAX_LOOP_COUNT:
            break

        tnow = time.time()   # epoch time, float
        wait_time = float(POLL_PERIOD) - (tnow % float(POLL_PERIOD))

        print("tnow:      %12.6f" % tnow)
        print("wait_time: %12.6f" % wait_time)
        print("%d - waiting" % loop_count)
        time.sleep(wait_time)
        my_response = requests.get(URL)
        if my_response.ok:
            sz = len(my_response.content)
            print("sz: %d" % sz)
            print(my_response.content)
            #print(my_response)
            analyze(my_response.content)
        else:
            my_response.raise_for_status()


if __name__ == '__main__':
    argc = len(sys.argv)
    main()
    sys.exit(0)


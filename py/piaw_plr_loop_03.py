#!/usr/bin/env python
"""
Loop to periodically poll the PiAware
Retrieve data from PiAware via REST interface
(preliminary analysis - track all hex number, figure out the different records)
todo: write to file
"""
import sys
import requests
import json
import time

URL = 'http://192.168.1.208:8080/data/aircraft.json'
POLL_PERIOD = 10     # seconds, must be integer > 0, should be 1,2,3,4,5,10,15,20,30, or 60
WAIT_OFFSET = 0.0

loop_count = 0
while True:
    loop_count += 1

    tnow = time.time()   # epoch time, float
    #time_since_last_poll = tnow % float(POLL_PERIOD)
    #wait_time = float(POLL_PERIOD) - time_since_last_poll
    wait_time = float(POLL_PERIOD) - (tnow % float(POLL_PERIOD))

    print("tnow:      %12.6f" % tnow)
    print("wait_time: %12.6f" % wait_time)
    print("%d - waiting" % loop_count)
    time.sleep(wait_time)
    if loop_count > 10:
        break
    myResponse = requests.get(URL)
    if myResponse.ok:
        sz = len(myResponse.content)
        print("sz: %d" % sz)
        print(myResponse.content)
        print(myResponse)
    else:
        myResponse.raise_for_status()


sys.exit(0)

#!/usr/bin/env python
"""
Loop to periodically poll the PiAware
(preliminary analysis - track all hex number, figure out the different records)
"""
import sys
import requests
import json
import time

URL = 'http://192.168.1.208:8080/data/aircraft.json'
POLL_PERIOD = 10     # seconds, must be integer > 0
                     # should be 1,2,3,4,5,10,15,20,30, or 60
WAIT_OFFSET = 0.0

tnow = time.time()   # epoch time, float
print("tnow:      %12.6f" % tnow)

#time_since_last_poll = tnow % float(POLL_PERIOD)
#wait_time = float(POLL_PERIOD) - time_since_last_poll

wait_time = float(POLL_PERIOD) - (tnow % float(POLL_PERIOD))

print("time_since_last_poll: %12.6f" % time_since_last_poll)
print("wait_time: %12.6f" % wait_time)



sys.exit(0)





myResponse = requests.get(URL)

print(myResponse)

if myResponse.ok:
    sz = len(myResponse.content)
    print("sz: %d" % sz)
    print(myResponse.content)

else:
    myResponse.raise_for_status()

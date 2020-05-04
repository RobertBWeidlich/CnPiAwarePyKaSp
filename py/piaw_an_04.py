#!/usr/bin/env python
"""
Loop to periodically poll the PiAware
Retrieve data from PiAware via REST interface
preliminary analysis - track all hex number, figure out the different records
"""
import sys
import requests
import socket
import json
import time

URL = 'http://192.168.1.208:8080/data/aircraft.json'
POLL_PERIOD = 10     # seconds, must be integer > 0, should be 1,2,3,4,5,10,15,20,30, or 60
WAIT_OFFSET = 0.0
MAX_LOOP_COUNT = 4


"""
Analyze data, which is expected to be in JSON format
"""
def analyze(json_data):
    data = json.loads(json_data)
    #print(data)
    d_now = data['now']
    #print("d_now: %f" % d_now)
    d_msg_count = data['messages']
    #print('d_msg_count: %d' % d_msg_count)
    d_aircraft_list = data['aircraft']
    hex_list = []
    for aircraft in d_aircraft_list:
        #print(aircraft)
        if 'hex' in aircraft:
            hex_list.append(aircraft['hex'])
    hex_list.sort()
    print(hex_list)


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


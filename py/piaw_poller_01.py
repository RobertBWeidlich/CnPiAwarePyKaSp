#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
file:   piaw_poller_01.py
author: rbw
date:   Sat Jun 13 19:43:22 EDT 2020
purpose:
  Loop to periodically poll the PiAware and save in file
"""
import sys
import os
import time
import requests
import math

POLL_PERIOD = 10     # seconds, must be integer > 0, should be 1,2,3,4,5,10,15,20,30, or 60
WAIT_OFFSET = 0.0
MAX_LOOP_COUNT = 10000000
URL = 'http://192.168.1.208:8080/data/aircraft.json'
BASE_DATA_DIR = '/data/piaware'
BASE_FILE_NAME = 'piaware_raw-'


def get_current_time_info(tz='local',base_dir=BASE_DATA_DIR):
    """
    :param: tz - 'local' or 'gmt'
    :param: base_dir - build data subdirectory with separate directories for
              YYYY, MM, DD, and HH
    :return: dictionary of timestamp-based data:
      timestamp: timestamp string in the form "YYYYMMDD.HHMM.SS.MILLIS"
                                        e.g., "20200624.2328.50.017823"
      directory: data directory
      file: data file name
      path: full pathname of data file
    """
    rv = {}
    tt_epoch = time.time()
    t_f = None
    if tz == 'local':
        t_f = time.localtime()
    else:
        t_f = time.gmtime(tt_epoch)
    millisecs = int(math.modf(tt_epoch)[0] * 1000000)
    type(millisecs)
    ts = '%04d%02d%02d.%02d%02d.%02d.%06d' %\
         (t_f.tm_year, t_f.tm_mon, t_f.tm_mday,
          t_f.tm_hour, t_f.tm_min,
          t_f.tm_sec, millisecs)
    rv['timestamp'] = ts

    dir = base_dir
    if not dir.endswith(os.sep):
        dir += os.sep
    dir = '%s%04d%s%02d%s%02d%s%02d' % \
          (dir,
           t_f.tm_year, os.sep,
           t_f.tm_mon, os.sep,
           t_f.tm_mday, os.sep,
           t_f.tm_hour)
    rv['directory'] = dir

    file = '%s%s%s' % (BASE_FILE_NAME, ts, '.json')
    rv['file'] = file

    path = '%s%s%s' % (dir, os.sep, file)
    rv['path'] = path

    return rv


def main():
    loop_count = 0;
    while True:
        loop_count += 1
        """
        1. Wait
        """
        tnow = time.time()  # epoch time, float
        wait_time = float(POLL_PERIOD) - (tnow % float(POLL_PERIOD))
        print("tnow:      %12.6f" % tnow)
        print("wait_time: %12.6f" % wait_time)
        print("%d - waiting" % loop_count)
        time.sleep(wait_time)
        print("here...")
        my_response = requests.get(URL)

        """
        2. Poll
        """
        pa_data = None
        if my_response.ok:
            sz = len(my_response.content)
            print("sz: %d" % sz)
            pa_data = my_response.content
            pa_data_sz = len(pa_data)
            #print(my_response.content)
            # print(my_response)
            print("pa_data_sz: %d" % pa_data_sz)
            print("pa_data: ")
            print(pa_data)
        else:
            my_response.raise_for_status()
        if not pa_data:
            continue

        """
        3. Generate timestamp and associated info
        """
        ts_info = get_current_time_info(tz='local')
        print("ts_info: %s" % ts_info)

        """
        4. Create subdirectory, if necessary
        """
        if not os.path.exists(ts_info['directory']):
            print("creating directory \'%s\'", ts_info['directory'])
            os.makedirs(ts_info['directory'])

        """
        5. Write data
        """
        with open(ts_info['path'], 'wb') as out_file:
            out_file.write(pa_data)


if __name__ == '__main__':
    argc = len(sys.argv)
    main()
    sys.exit(0)

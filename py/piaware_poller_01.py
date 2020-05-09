#!/usr/bin/env python
"""
Retrieve data from PiAware via REST interface
"""
import sys
import requests
import json

print("Hello World!")

URL = 'http://192.168.1.208:8080/data/aircraft.json'

myResponse = requests.get(URL)

print(myResponse)

if myResponse.ok:
    sz = len(myResponse.content)
    print("sz: %d" % sz)
    print(myResponse.content)

else:
    myResponse.raise_for_status()


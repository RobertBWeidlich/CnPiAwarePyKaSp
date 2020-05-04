# CnPiAwarePyKaSp
Periodically poll PiAware data, push to Kafka, and analyze with Spark Stream Processing

* if we poll every second, we will have
    60 * 24 * 60 = 86,400 records per day
    
* If we poll every 3 seconds, we will have
    60 * 24 * 20 = 28,800 records per day

* If we poll every 5 seconds, we will have
    60 * 24 * 12 = 17,280 records per day

* If we poll every 6 seconds, we will have
    60 * 24 * 10 = 14,400 records per day
    
* If we poll every 10 seconds, we will have
    60 * 24 * 6 = 8640 records per day
    60 MB of data per day, assuming payload
    of 7000 bytes
    

    
    

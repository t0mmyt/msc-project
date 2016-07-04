#!/usr/bin/env python3.5
from observation import Observation, ObservationError
from os.path import join as path_join
from os import walk
from sys import exit
# Graphite specific
# import socket
from datastore.opentsdb import OpenTSDB

WORKDIR = "/home/tom/code/msc-project/data/sample"

filelist = []
for root, dirs, files in walk(WORKDIR):
    for filename in files:
        if filename[-4:].upper() == ".SAC":
            filelist.append((path_join(root, filename)))

# a = filelist.index(
#    '/srv/seismic_raw/2012.238/2012.238.00.00.00.0000.YW.NAB2..BHN.D.SAC')
a = 0
remaining = filelist[a + 1:]

# set time-series datastore
ts = OpenTSDB(host='172.16.1.90')
for path in remaining:
    try:
        my_obs = Observation(path=path)
    except ObservationError as e:
        print("Error happened reading: {}".format(e))
        exit(1)

#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.connect(('127.0.0.1', 2003))
    meta = my_obs.meta()
    for i in my_obs.data_with_time():
        ts.send(
            metric=meta['channel'],
            value=i[1],
            timestamp=i[0],
            network=meta['network'],
            station=meta['station'])

#    for i in my_obs.graphite_text():
#        s.send(i.encode())
#    s.close()
    print("{} loaded".format(path))
ts.close()

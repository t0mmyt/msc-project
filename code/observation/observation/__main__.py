#!/usr/bin/env python3.5
from os import getenv
from io import BytesIO
import cherrypy as cp

from tsdatastore.opentsdb import OpenTSDB
from observation.api import ObservationLoader

OPENTSDB = getenv('OPENTSDB')
LISTEN_HOST = getenv('OBSAPI_LISTEN_HOST', "0.0.0.0")
LISTEN_PORT = int(getenv('OBSAPI_LISTEN_PORT', 8010))
assert OPENTSDB, "OPENTSDB environment variable must be set"

tsdb = OpenTSDB(OPENTSDB)

cp.tree.mount(ObservationLoader(tsdb=tsdb), '/')
cp.server.socket_host = "0.0.0.0"
cp.server.socket_port = 8001
cp.engine.timeout_monitor.unsubscribe()
cp.engine.start()
cp.engine.block()

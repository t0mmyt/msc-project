#!/usr/bin/env python3
from os import getenv, environ
import cherrypy as cp

from tsdatastore.opentsdb import OpenTSDB
from tsdatastore.api import TSDBHandler, TSDBList

OPENTSDB = getenv('OPENTSDB')
LISTEN_HOST = getenv('TSDBAPI_LISTEN_HOST', "0.0.0.0")
LISTEN_PORT = int(getenv('TSDBAPI_LISTEN_PORT', 8010))
assert OPENTSDB, "OPENTSDB environment variable must be set"

tsdb = OpenTSDB(OPENTSDB)

cp.tree.mount(
    TSDBHandler(tsdb), '/', {
        '/': {
            'request.dispatch': cp.dispatch.MethodDispatcher()
        }
    }
)
cp.tree.mount(TSDBList(tsdb), '/list')

cp.server.socket_host = LISTEN_HOST
cp.server.socket_port = LISTEN_PORT
cp.engine.start()
cp.engine.block()

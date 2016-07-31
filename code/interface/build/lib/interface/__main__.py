#!/usr/bin/env python3
from os import getenv
import cherrypy as cp

from interface.gui import GUI
from interface.ajax import Ajax

LISTEN_HOST = getenv('OBSAPI_LISTEN_HOST', "0.0.0.0")
LISTEN_PORT = int(getenv('OBSAPI_LISTEN_PORT', 8000))
TSDBAPI = getenv('TSDBAPI')
assert TSDBAPI, "TSDBAPI environment variable must be set"


cp.tree.mount(GUI(), '/')
cp.tree.mount(Ajax(TSDBAPI), '/ajax')

cp.server.socket_host = LISTEN_HOST
cp.server.socket_port = LISTEN_PORT
cp.engine.start()
cp.engine.block()

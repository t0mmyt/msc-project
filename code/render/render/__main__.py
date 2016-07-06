#!/usr/bin/env python3.5
from os import getenv
import cherrypy as cp

from render.graph import HTTPRender

TSDBAPI_HOST = getenv('TSDBAPI_HOST')
TSDBAPI_PORT = int(getenv('TSDBAPI_PORT'))
LISTEN_HOST = getenv('RENDER_LISTEN_HOST', "0.0.0.0")
LISTEN_PORT = int(getenv('RENDER_LISTEN_PORT', 8002))
assert TSDBAPI_HOST, "TSDBAPI_HOST environment variable must be set"
assert TSDBAPI_PORT, "TSDBAPI_PORT environment variable must be set"

cp.tree.mount(HTTPRender((TSDBAPI_HOST, TSDBAPI_PORT)), '/')
cp.server.socket_host = LISTEN_HOST
cp.server.socket_port = LISTEN_PORT
cp.engine.start()
cp.engine.block()

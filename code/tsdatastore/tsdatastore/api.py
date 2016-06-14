#!/usr/bin/env python3
from tsdatastore.opentsdb import OpenTSDB
import cherrypy as cp
from cherrypy import tools
import json

OPENTSDB = "172.16.1.90"


class TSDBHandler(object):
    exposed = True

    def __init__(self, tsdb):
        self.tsdb = tsdb

    @cp.tools.allow(methods=['GET'])
    @tools.json_out()
    def GET(self, metric, start, end, **tags):
        query = tags
        query.update({
            "start": float(start),
            "end": float(end),
            "metric": metric,
        })
        t, v = tsdb.read(**query)
        return dict(t=t, v=v)


class TSDBList(object):
    def __init__(self, tsdb):
        self.tsdb = tsdb

    @cp.expose
    @tools.json_out()
    def index(self, metric, **tags):
        return tsdb.lookup(metric=metric, **tags)


if __name__ == '__main__':
    tsdb = OpenTSDB(host=OPENTSDB)

    cp.tree.mount(
        TSDBHandler(tsdb), '/', {
            '/': {
                'request.dispatch': cp.dispatch.MethodDispatcher()
            }
        }
    )
    cp.tree.mount(TSDBList(tsdb), '/list')

    cp.server.socket_host = "0.0.0.0"
    cp.server.socket_port = 8010
    cp.engine.start()
    cp.engine.block()

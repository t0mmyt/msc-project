#!/usr/bin/env python3
from opentsdb import OpenTSDB
import cherrypy as cp
import json

OPENTSDB = "172.16.1.90"


class TSDBHandler(object):
    exposed = True

    def __init__(self, tsdb):
        self.tsdb = tsdb

    def GET(self, metric, start, end, **tags):
        query = tags
        query.update({
            "start": float(start),
            "end": float(end),
            "metric": metric,
        })
        t, v = tsdb.read(**query)
        return json.dumps(dict(t=t, v=v))


if __name__ == '__main__':
    tsdb = OpenTSDB(host=OPENTSDB)

    cp.tree.mount(
        TSDBHandler(tsdb), '/', {
            '/': {
                'request.dispatch': cp.dispatch.MethodDispatcher()
            }
        }
    )

    cp.server.socket_host = "0.0.0.0"
    cp.server.socket_port = 8010
    cp.engine.start()
    cp.engine.block()

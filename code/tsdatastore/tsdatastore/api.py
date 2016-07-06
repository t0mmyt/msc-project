#!/usr/bin/env python3
import json
import cherrypy as cp

from tsdatastore.opentsdb import OpenTSDB

OPENTSDB = "opentsdb"


class TSDBHandler(object):
    exposed = True

    def __init__(self, tsdb):
        self.tsdb = tsdb

    @cp.tools.allow(methods=['GET'])
    @cp.tools.json_out()
    def GET(self, metric, start, end, **tags):
        query = tags
        query.update({
            "start": float(start),
            "end": float(end),
            "metric": metric,
        })
        t, v = self.tsdb.read(**query)
        return dict(t=t, v=v)


class TSDBList(object):
    def __init__(self, tsdb):
        self.tsdb = tsdb

    @cp.expose
    @cp.tools.json_out()
    def index(self, metric, **tags):
        return self.tsdb.lookup(metric=metric, **tags)

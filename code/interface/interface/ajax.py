import cherrypy as cp
import requests

class Ajax(object):
    @cp.expose
    def list(self, metric=None, network=None, station=None):
        pass

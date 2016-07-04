#!/usr/bin/env python3
import cherrypy as cp
from jinja2 import Environment, FileSystemLoader
import requests
env = Environment(loader=FileSystemLoader('templates'))

HTTP_RENDER = ("172.16.1.2", 8001)
TSDB_API = ('172.16.1.2', 8010)


class GUI(object):
    @cp.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render()

    @cp.expose
    def explore(self):
        return "Explore"


class Ajax(object):
    @cp.expose
    def list(self, metric=None, network=None, station=None):
        pass

# class UserInterface(object):
#     @cherrypy.expose
#     def index(self, network, station, start, end):
#         params = {
#             'start': start,
#             'end': end,
#             'station': station,
#             'network': network,
#         }
#
#         raw_render = self._get_render('sax', params)
#
#         if raw_render:
#             cherrypy.response.headers['Content-Type'] = "image/png"
#             return raw_render
#         return "Error happened"
#
#     def _get_render(self, render_type, params):
#         url = "http://{}:{}/{}".format(*HTTP_RENDER, render_type)
#         r = requests.get(url, params=params)
#         if r.status_code != 200:
#             return None
#         return r.content
#
#
if __name__ == '__main__':
    cp.tree.mount(GUI(), '/')
    cp.tree.mount(Ajax(), '/ajax')

    cp.server.socket_host = "0.0.0.0"
    cp.server.socket_port = 8000
    cp.engine.start()
    cp.engine.block()

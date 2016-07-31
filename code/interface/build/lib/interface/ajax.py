import cherrypy as cp
import requests
import json

class Ajax(object):
    def __init__(self, tsdbapi):
        self.tsdbapi = tsdbapi

    @cp.expose
    @cp.tools.json_out()
    def list_params(self, **params):
        url = "http://{}/list".format(self.tsdbapi)
        r = requests.get(url=url, params=params)
        o = r.json()
        response = dict()
        for i in o[params['metric']]:
            if i['network'] not in response:
                response[i['network']] = []
            response[i['network']].append(i['station'])
        response[i['network']].sort()
        return response

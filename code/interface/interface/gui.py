import cherrypy as cp
from jinja2 import Environment, FileSystemLoader, Template
import requests
import json
import datetime as dt
from io import BytesIO
from urllib.parse import urlencode

# TODO pass as __init__
env = Environment(loader=FileSystemLoader('/opt/code/interface/templates'))


class NavBar(object):
    def __init__(self, template, items):
        self.template = env.get_template(template)
        self.items = items
        env.get_template('index.html.j2')

    def render(self, active):
        return self.template.render(items=self.items, active=active, title="Seismic Shift")


class GUI(object):
    menu = [
        ('Import', "/importer" ),
        ('Explore', "/explore"),
        ('SAX', "/sax"),
    ]
    tmpl = env.get_template('index.html.j2')

    @cp.expose
    def index(self):
        nav = NavBar('nav_container.html.j2', self.menu)
        return self.tmpl.render(navbar=nav.render(active='Home'))

    @cp.expose
    def importer(self, **params):
        response=[]
        if cp.request.method == "POST":
            if "input_file" in params:
                if not isinstance(params['input_file'], list):
                    files = [params['input_file']]
                else:
                    files = params['input_file']

                for f in files:
                    data = f.file.read()
                    r = requests.post(
                        "http://observation:8001",
                        headers={'Content-Type': "application/octet"},
                        data=data
                    )
                    if 200 <= r.status_code <= 299:
                        response.append(r.json())
                    else:
                        response.append(dict(error="observation returned {}".
                                             format(r.status_code)))
            else:
                response.append(dict(error="No files found"))
        elif cp.request.method == "GET":
            pass
        nav = NavBar('nav_container.html.j2', self.menu)
        body_tmpl = env.get_template('importer.html.j2')
        if len(response) == 0:
            response = ""
        else:
            response = json.dumps(response, indent=2)
        return self.tmpl.render(
            navbar=nav.render(active='importer'),
            body=body_tmpl.render(response=response),
        )

    @cp.expose
    def explore(self, **params):
        content = None
        form_keys = ('network', 'station', 'channel', 'startD', 'endD',
                     'startT', 'endT')
        form = dict()
        for k in form_keys:
            form[k] = params[k] if k in params else ""
        error = []

        if all(key in params for key in form_keys):
            print(json.dumps(params))
            start = GUI.to_datetime(params['startD'], params['startT'])
            end = GUI.to_datetime(params['endD'], params['endT'])
            if not start:
                error.append({'error': "Start date or time not understood"})
            if not end:
                error.append({'error': "End date or time not understood"})
            if start and end:
                qry_params = dict(
                    network=params['network'],
                    station=params['station'],
                    channel=params['channel'],
                    start=start.timestamp(),
                    end=end.timestamp()
                )
                content = """<a href='/sax?{}'>
                    <img width=\"100%\" src=\"/render_raw?{}\">
                    </a>""".format(
                    urlencode(params),urlencode(qry_params))
        nav = NavBar('nav_container.html.j2', self.menu)
        body_tmpl = env.get_template('explore.html.j2')
        return self.tmpl.render(
            navbar=nav.render(active='Explore'),
            body=body_tmpl.render(
                form=form,
                content=content,
                error=json.dumps(error, indent=2) if len(error) > 0 else None,
            )
        )

    @cp.expose
    def sax(self, **params):
        content = None
        form_keys = ('network', 'station', 'channel', 'startD', 'endD',
                     'startT', 'endT')
        form_defaults = {
            'paa_int': 50,
            'alphabet': "abcdefg",
        }
        form = dict()
        for k in form_keys:
            form[k] = params[k] if k in params else ""
        error = []
        for k, v in form_defaults.items():
            form[k] = params[k] if k in params else v

        if all(key in params for key in form_keys):
            print(json.dumps(params))
            start = GUI.to_datetime(params['startD'], params['startT'])
            end = GUI.to_datetime(params['endD'], params['endT'])
            if not start:
                error.append({'error': "Start date or time not understood"})
            if not end:
                error.append({'error': "End date or time not understood"})
            if start and end:
                qry_params = dict(
                    network=form['network'],
                    station=form['station'],
                    channel=form['channel'],
                    start=start.timestamp(),
                    end=end.timestamp(),
                    interval=form['paa_int'],
                    alphabet=form['alphabet'],
                )
                # content = "<img width=\"100%\" src=\"/render_sax?{}\">".format(urlencode(qry_params))
                content = """<a href='/saxstr?{0}'>
                    <img width=\"100%\" src=\"/render_sax?{0}\">
                    </a>""".format(
                    urlencode(qry_params))

        nav = NavBar('nav_container.html.j2', self.menu)
        body_tmpl = env.get_template('sax.html.j2')
        return self.tmpl.render(
            navbar=nav.render(active='SAX'),
            body=body_tmpl.render(
                form=form,
                content=content,
                error=json.dumps(error, indent=2) if len(error) > 0 else None,
            )
        )


    @cp.expose
    def render_raw(self, **params):
        ct, c = self.render_pass('raw', **params)
        cp.response.headers['Content-Type'] = ct
        return c

    @cp.expose
    def render_sax(self, **params):
        ct, c = self.render_pass('sax', **params)
        cp.response.headers['Content-Type'] = ct
        return c

    @cp.expose
    def saxstr(self, **params):
        ct, c = self.render_pass('saxstr', **params)
        cp.response.headers['Content-Type'] = ct
        return c

    def render_pass(self, path, **params):
        # ConnectionRefusedError
        r = requests.get("http://render:8002/{}".format(path), params=params)
        ram = BytesIO(r.content)
        ram.seek(0)
        return r.headers['Content-Type'], ram.read()

    @staticmethod
    def to_datetime(d, t):
        dt_str = " ".join((d, t))
        try:
            my_dt = dt.datetime.strptime(dt_str, "%Y/%m/%d %H:%M:%S")
        except ValueError:
            return None
        return my_dt

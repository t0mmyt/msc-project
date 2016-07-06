import cherrypy as cp
from jinja2 import Environment, FileSystemLoader

# TODO pass as __init__
env = Environment(loader=FileSystemLoader('/opt/code/interface/templates'))


class GUI(object):
    @cp.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render()

    @cp.expose
    def explore(self):
        return "Explore"

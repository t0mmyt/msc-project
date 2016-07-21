#!/usr/bin/env python3
from jinja2 import Template

menu = [
    ('Home', "/" ),
    ('Import', "/import" ),
    ('Explore', "/explore"),
    ('SAX', "/sax"),
]

template = \
"""
<nav class="navbar navbar-inverse navbar-fixed-top">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">Seismic Shift</a>
    </div>
    <div id="navbar" class="navbar-collapse collapse">
      <ul class="nav navbar-nav">
        {% for item in items -%}
          {% if item[0] is string -%}
        <li><a href="{{ item[1] }}">{{ item[0] }}</a></li>
          {% endif -%}
        {% endfor -%}
      </ul>
    </div><!--/.nav-collapse -->
  </div>
</nav>
"""


class NavBar(object):
    def __init__(self, template, items):
        self.template = Template(template)
        self.items = items

    def render(self):
        print(self.items)
        return self.template.render(items=self.items, active="Home")

n = NavBar(template, menu)
print(n.render())

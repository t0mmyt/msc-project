#!/usr/bin/env python3
from datastore import InfluxDB
import cStringIO
import numpy as np
from sax import Paa, Sax
import plotly
from plotly.graph_objs import Scatter, Bar, Layout
from obspy.signal.filter import highpass, lowpass
import matplotlib as mpl
mpl.use('agg')
from matplotlib import pyplot as plt
from flask import flask

app = Flask(__name__)
from app import views


@app.route('/')
def index():
    i = InfluxDB('127.0.0.1', 'admin', 'admin', 'graphite')

    my_time, my_value = i.query(
        'yw', 'nab2', 'hhz',
        '2011-09-11 19:30:55',
        '2011-09-11 19:31:05')

    my_value = highpass(
        data=my_value,
        freq=1,
        df=500
    )
    # my_value = lowpass(
    #     data=my_value,
    #     freq=10,
    #     df=100
    # )

    # interval for Paa
    i = 100
    p = Paa(my_time, my_value, i)
    s = Sax(p, "abcde")

    # plotly.offline.plot({
    #     "data": [
    #         Scatter(x=Paa.as_time(s.paa.in_time), y=s.paa.normalised),
    #         Bar(x=s.paa.times, y=s.paa.values),
    #     ],
    # })
    ram = cStringIO.StringIO()
    fig, ax = plt.subplots()
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=30, fontsize=10)
    plt.plot(p.as_time(p.in_time), p.normalised, color='g')
    plt.step(p.as_time(np.add(p.epoch, i)), p.values, color='b', linewidth=2)
    plt.axhline(0, color='black')
    plt.grid(b=True, which='major', color='grey', linestyle='-')
    for y in s.breakpoints:
        plt.axhline(y, color='red')
    for i in range(len(s.sax_str)):
        plt.text(
            s.paa.times[i], 0,
            s.sax_str[i], va='center', ha='center')
    plt.savefig(ram)
    plt.close()
    return Response(ram.read(), mimetype='image/png')

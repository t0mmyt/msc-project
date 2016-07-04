#!/usr/bin/env python3
from io import BytesIO
from obspy.signal.filter import bandpass
import datetime as dt
import cherrypy as cp
import numpy as np
import requests
from sax import Paa, Sax
import matplotlib as mpl
mpl.use('agg')
from matplotlib import pyplot as plt

TSDB_API = ('172.16.1.2', 8010)


class HTTPRender(object):
    @cp.expose
    def raw(self, start, end, station, network):
        cp.response.headers['Content-Type'] = "image/png"

        ts = self._get(
            metric='Z',
            start=start,
            end=end,
            station=station,
            network=network
        )
        t = np.array(ts['t'])
        v = np.array(ts['v'])

        # TODO - move this!
        # v = highpass(data=v, freq=1000, df=50)
        # TODO - why is lowpass not working?
        # v = lowpass(data=v, freq=10, df=50)

        ram = BytesIO()
        fig, ax = plt.subplots()
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=10, fontsize=10)
        plt.plot(t, v, color='b', lw=.25)
        plt.axhline(0, color='black')
        plt.grid(b=True, which='major', color='grey', ls='-')
        plt.savefig(ram, format='png')
        plt.close()
        ram.seek(0)
        return ram.read()

    @cp.expose
    def sax(
            self, start, end, station, network,
            interval=50, alphabet="abcdefghi", lp=1, hp=20):
        cp.response.headers['Content-Type'] = "image/png"

        ts = self._get(
            metric='Z',
            start=start,
            end=end,
            station=station,
            network=network
        )
        t = np.array(ts['t'])
        v = np.array(ts['v'])

        start_dt = dt.datetime.fromtimestamp(float(start))

        # TODO - move this! - maybe
        v = bandpass(data=v, freqmin=lp, freqmax=hp, df=50)

        p = Paa(t, v, interval)
        s = Sax(p, alphabet)

        ram = BytesIO()
        fig = plt.figure(figsize=(14, 8), dpi=100, facecolor='black')
        fig.suptitle("{}.{} {}".format(
            network, station, start_dt.strftime("%Y-%m-%d")), color='white')
        title1 = "SAX (PAA Interval: {}ms, alphabet: {})".format(
            interval, len(alphabet))
        title2 = "Raw (Bandpass {}/{}Hz)".format(lp, hp)
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        ax1.set_title(label=title1, color='white')
        ax2.set_title(label=title2, color='white')
        ax1.step(p.as_time(p.paa_time), p.paa_value, color='lime', lw=1)
        ax2.plot(p.as_time(p.in_time), p.in_value, color='c', lw=1)
        for ax in (ax1, ax2):
            plt.setp(
                ax.get_xticklabels(), rotation=10, fontsize=8, color='white')
            plt.setp(
                ax.get_yticklabels(), fontsize=8, color='white')
            ax.minorticks_on()
            ax.grid(b=True, which='major', color='grey', ls='-', lw=1)
            ax.grid(b=True, which='minor', color='grey', ls=':', lw=.5)
            ax.set_axis_bgcolor('black')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')

        ax1.set_ylim(
            s.breakpoints[0] - (s.breakpoints[1] - s.breakpoints[0]) / 2,
            s.breakpoints[-1] + (s.breakpoints[-1] - s.breakpoints[-2]) / 2,
        )
        a = 0
        for y in s.breakpoints:
            ax1.axhline(y, color='darkred', lw=.75)
            ax1.text(
                s.paa.times[0], y, va='center', color='darkred',
                s=" {}\n {}".format(alphabet[a + 1], alphabet[a]))
            a += 1

        # for i in range(1, len(s.sax_str)):
        #     plt.text(
        #         s.paa.times[i] - dt.timedelta(milliseconds=(interval/2)), 0,
        #         s.sax_str[i], va='center', ha='center',
        #         family='monospace', weight='bold', size=8)
        plt.savefig(ram, format='png', facecolor='black')
        plt.close()
        ram.seek(0)
        return ram.read()

    def _get(self, metric, **kwargs):
        url = "http://{}:{}/{}".format(*TSDB_API, metric)
        r = requests.get(url, params=kwargs)
        if r.status_code != 200:
            return None
        return r.json()


# class Plot(object):
#     @staticmethod
#     def align_yaxis(ax1, v1, ax2, v2):
#         """
#         Adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1
#         taken from http://stackoverflow.com/a/26456731
#         """
#         _, y1 = ax1.transData.transform((0, v1))
#         _, y2 = ax2.transData.transform((0, v2))
#         Plot.adjust_yaxis(ax2, (y1 - y2) / 2, v2)
#         Plot.adjust_yaxis(ax1, (y2 - y1) / 2, v1)
#
#     @staticmethod
#     def adjust_yaxis(ax, ydif, v):
#         """
#         Shift axis ax by ydiff, maintaining point v at the same location
#         taken from http://stackoverflow.com/a/26456731
#         """
#         inv = ax.transData.inverted()
#         _, dy = inv.transform((0, 0)) - inv.transform((0, ydif))
#         miny, maxy = ax.get_ylim()
#         miny, maxy = miny - v, maxy - v
#         if -miny > maxy or (-miny == maxy and dy > 0):
#             nminy = miny
#             nmaxy = miny*(maxy+dy)/(miny+dy)
#         else:
#             nmaxy = maxy
#             nminy = maxy*(miny+dy)/(maxy+dy)
#         ax.set_ylim(nminy+v, nmaxy+v)

if __name__ == '__main__':
    cp.tree.mount(HTTPRender(), '/')

    cp.server.socket_host = "0.0.0.0"
    cp.server.socket_port = 8001
    cp.engine.start()
    cp.engine.block()

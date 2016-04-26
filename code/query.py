#!/usr/bin/env python3
from datastore import InfluxDB
from matplotlib import pyplot as plt
import numpy as np


class Sax(object):
    def __init__(self, time, value, interval, alphabet):
        self.time = time
        self.value = value
        self.interval = interval
        self.n = 2 * int(((time[-1:] - time[0]) / self.interval) + .5)
        self.sax_time = np.empty(self.n)
        self.sax_value = np.empty(self.n)
        self.alphabet = tuple(alphabet)
        self._calc()

    def _calc(self):
        t = self.time
        v = self.value
        interval = t[0]
        n = 0
        while interval < t[-1:]:
            index_start = np.searchsorted(t, interval)
            t_start = t[index_start]
            t_end = t_start + self.interval
            index_end = np.searchsorted(t, t_end)
            interval += self.interval
            mean = np.mean(v[index_start:index_end])
            self.sax_time[2 * n] = t_start
            self.sax_value[2 * n] = mean
            self.sax_time[2 * n + 1] = t_end - 1
            self.sax_value[2 * n + 1] = mean
            n += 1

    @property
    def times(self):
        return self.sax_time

    @property
    def values(self):
        return self.sax_value


i = InfluxDB('127.0.0.1', 'admin', 'admin', 'graphite')

my_time, my_value = i.query(
    'yw', 'nab1', 'bhz',
    '2012-02-05 12:00:00',
    '2012-02-05 12:30:00')

s = Sax(my_time, my_value, 60000, "abcde")

plt.plot(s.times, s.values)
plt.show("/home/tom/graph.png")

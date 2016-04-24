#!/usr/bin/env python3.5
from observation.exceptions import ObservationException
from obspy import read as obs_read
from logging import debug
from decimal import Decimal     # To get around floating point inaccuracy
from iso8601 import parse_date


class Observation(object):
    """
    Observation contains is able to read an observation from disk and pass to a
    time-series datastore.
    """
    def __init__(self, path=None):
        """
        Create a new observation object and call read_from_disk with given path

        Parameters
        ----------
        path : string
            Path to observation file
        """
        if path:
            self.stream = self.read_from_disk(path)
            if not self.stream:
                raise ObservationException('Could not read observation')
        else:
            raise ObservationException(
                    'No method to read stream, try passing a path')

    @staticmethod
    def read_from_disk(path):
        """
        Reads a SAC file using obspy and stores as self.stream

        Parameters
        ----------
        path : string
            Path to observation file
        """
        debug('Attempting to open ({})'.format(path))
        try:
            stream = obs_read(path)
        except (IOError) as e:
            raise ObservationException('Failed to read {}: {}'.format(path, e))
        return stream

    @property
    def trace_count(self):
        """
        Return the number of traces in the stream
        """
        return len(self.stream)

    def data_with_time(self, tracenum=0):
        """
        Generator to return tuples of (timestamp, metric)

        Parameters
        ----------
        trace : int
            trace number to iterate through, default 0
        """
        trace = self.stream[tracenum]
        starttime = Decimal(parse_date(str(
            trace.stats.starttime)).timestamp())
        interval = Decimal(1 / float(trace.stats.sampling_rate))
        ts = starttime
        for n in trace.data:
            yield tuple((ts, n))
            ts += interval

    def meta(self, tracenum=0):
        """
        Return a list of tuples (timestamp, metric)

        Parameters
        ----------
        trace : int
            trace number to iterate through, default 0
        """
        trace = self.stream[tracenum]
        return trace.stats

    def graphite_text(self, tracenum=0):
        """
        Generator to return graphite formatted output of trace. Metric path is
        network.station.channel

        Parameters
        ----------
        trace : int
            trace number to iterare through, default 0
        """
        trace = self.stream[tracenum]
        starttime = Decimal(parse_date(str(
            trace.stats.starttime)).timestamp())
        interval = Decimal(1 / float(trace.stats.sampling_rate))
        ts = starttime
        metric = '.'.join((
            trace.stats.network,
            trace.stats.station,
            trace.stats.channel
        )).lower()
        for n in trace.data:
            yield "{} {} {}\n".format(metric, n, ts)
            ts += interval

import math
import requests
import numpy as np


class OpenTSDB(object):
    """
    Datastore for accessing OpenTSDB
    """
    def __init__(self, host, port=4242, buffermax=20):
        """
        Esatiblish connection parameters for OpenTSDB (HTTP) interface.

        Parameters
        ----------
        host, port: string, int
        buffermax: int
            (default 20).  Used to batch together sending data to OpenTSDB.
            Set to 1 to emit each metric individually.  Flushed on close().
        """
        self.host = host
        self.port = port
        self.buffermax = buffermax
        self.buffer = []

    def send(self, metric, value, timestamp, **tags):
        """
        Send (or queue if buffer not full) metric(s) to OpenTSDB.

        Parameters
        ----------
        metric: string
            Name of metric
        value: number
            Value of metric
        timestamp: number
            Epoch time in seconds (float for subseconds)
        **tags: dict
            Additional tags to send
        """
        self.buffer.append({
            'metric': metric,
            'timestamp': int(timestamp * 1000),
            'value': int(value),
            'tags': tags
        })
        if len(self.buffer) >= self.buffermax:
            self._dump_payload()

    def _dump_payload(self):
        """
        Send contents of buffer and empty
        """
        r = requests.post(
            "http://{}:{}/api/put".format(self.host, self.port),
            json=self.buffer
        )
        if r.status_code != 204:
            print("Error!\n{}".format(r.text))
        self.buffer = []

    def close(self):
        """
        Final empty of buffer
        """
        if len(self.buffer) > 0:
            self._dump_payload()

    def read(self, metric, start, end, **tags):
        """
        Read data from OpenTSDB.  Returns two numpy arrays (Epoch time in ms
        and values)

        Parameters
        ----------
        metric: string
            Name of metric to retrieve
        start, end: number
            Epoch time (either s or ms)
        **tags: dict
            Additional tags
        """
        # always in ms
        if int(math.log10(start)) == 9:
            start *= 1000
        if int(math.log10(end)) == 9:
            end *= 1000
        # Build Query
        query = {
            'start': int(start),
            'end': int(end),
            'msResolution': True,
            'queries': [
                {
                    'aggregator': "avg",
                    'metric': metric,
                    'tags': tags
                }
            ]
        }
        # Submit query to OpenTSDB HTTP API
        r = requests.post(
            "http://{}:{}/api/query".format(self.host, self.port),
            headers={'Content-Type': "application/json; charset=UTF-8"},
            json=query
        )
        # TODO - Throw back exceptions!
        if r.status_code != 200:
            print("{}\n{}".format(r.status_code, r.json()))
        raw = r.json()[0]['dps']
        t = np.array(sorted(raw.keys()))
        v = np.zeros(len(t))
        j = 0
        for i in t:
            v[j] = raw[i]
            j += 1

        return t.astype(np.int).tolist(), v.tolist()

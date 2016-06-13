from influxdb import InfluxDBClient
import numpy as np
import operator


class InfluxDB(object):
    """
    Datastore class for accessing InfluxDB
    """
    def __init__(self, host, user, password, database):
        """
        Initialise connection to InfluxDB

        Parameters
        ----------
        host : string
            hostname (or IP) of InfluxDB instance
        user : string
            InfluxDB username
        password : string
            InfluxDB password
        database : string
            Databse to use in InfluxDB
        """
        self.client = InfluxDBClient(
            host=host,
            username=user,
            password=password,
            database=database
        )

    def query(self, network, station, channel, start, end):
        """
        Return datapoints for a given network/station/channel for a given
        time range.

        Parameters
        ----------
        network : string
        station : string
        channel : string
        start :
        end :
        """
        query = (
            "SELECT value FROM \"{}.{}.{}\" "
            "WHERE time >= '{}' "
            "AND time < '{}'".format(
                network, station, channel,
                start, end)
        )
        q = self.client.query(
            query,
            params={'epoch': 'ms'})
        print(query)
        a = ("{}.{}.{}".format(network, station, channel), None)
        fields = operator.itemgetter('time', 'value')
        r = list(zip(*[fields(i) for i in q[a]]))
        t = np.array(r[0])
        v = np.array(r[1])
        return t, v

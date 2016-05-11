from datetime import datetime as dt
import numpy as np


class Paa(object):
    """
    Class to perform PAA (Piecewise Aggregate Approximation)
    """
    def __init__(self, time, value, interval):
        """
        Create and calculate PAA

        Parameters
        ----------
        time : numpy.array
            Times in epoch ms
        value : numpy.array
            Y values
        interval : int
            Window size in ms
        """
        self.in_time = time
        self.in_value = value
        self.interval = interval
        # Calculate array size for results
        self.n = int(((time[-1:] - time[0]) / self.interval) + .5)
        self.paa_time = np.empty(self.n)
        self.paa_value = np.empty(self.n)
        # Normalise to zero
        self.normalised = self._normalise_to_zero(value)
        # Call calculation and get peak
        paa_max = self._calc()
        # Nomalise to peak
        self.normalised = self._normalise_peak(self.normalised, paa_max)
        self.paa_value = self._normalise_peak(self.paa_value, paa_max)

    @staticmethod
    def _normalise_to_zero(v):
        """
        Return numpy array normalised to zero by subtracting the mean from each
        value

        Parameters
        ----------
        v : numpy.array (1D)
            Array to normalise
        """
        mu = np.mean(v)
        v = np.subtract(v, mu)
        return v

    @staticmethod
    def _normalise_peak(v, peak):
        """
        Scale a numpy array so that the peak is 1 (or -1).
        The peak is passed as it is intended to be used from a different
        function (i.e. PAA in this case)

        Parameters
        ----------
        v : numpy.array (1D)
            Array to normalised
        peak : float
            Peak value to normalise from
        """
        return np.divide(v, peak)

    def _calc(self):
        """
        Perform PAA analysis and assign to self.paa_value against self.paa_time
        and return the peak value for normalisation
        """
        t = self.in_time
        v = self.normalised
        interval = t[0]
        n = 0
        # Iterate through dataset by interval
        while interval < t[-1:]:
            index_start = np.searchsorted(t, interval)
            t_start = t[index_start]
            t_end = t_start + self.interval
            index_end = np.searchsorted(t, t_end)
            interval += self.interval
            mean = np.mean(v[index_start:index_end])
            self.paa_time[n] = t_start
            self.paa_value[n] = mean
            n += 1
        return max(np.max(self.paa_value), 0 - np.min(self.paa_value))

    @staticmethod
    def as_time(t):
        """
        Convert a numpy.array of times from epoch to datetime objects
        """
        return np.array([dt.fromtimestamp(i/1000) for i in t])

    @property
    def epoch(self):
        """
        Return PAA times as epoch
        """
        return self.paa_time

    @property
    def times(self):
        """
        Return PAA times as datetimes
        """
        return self.as_time(self.epoch)

    @property
    def values(self):
        """
        Return PAA values
        """
        return self.paa_value

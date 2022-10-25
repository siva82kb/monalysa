"""
readers.py is a module with classes and functions to read data from different
wearable sensors that are commonly used for movement tracking applications.
"""

import pandas
from pandas import DataFrame
from pandas import Timestamp, Timedelta
from datetime import datetime as dt
import datetime


class ActiGraphData(object):
    """Class to handle the activity counts data from an ActiGraph sensor.
    """
    
    @staticmethod
    def read_organize_data(filename, header=10):
        """Function to read CSV ActiGraph data file.
        """
        _data = pandas.read_csv(filename, header=header, sep=",")
        _data.columns = [_c.strip() for _c in _data.columns]
        # Add a datetime columns
        _data['TimeStamp'] = _data["Date"] + _data['Time']
        _data['TimeStamp'] = _data['TimeStamp'].map(lambda x: dt.strptime(x, "%d/%m/%Y%H:%M:%S"))
        _data['Date'] = _data['TimeStamp'].map(lambda x: x.date())
        _data['Time'] = _data['TimeStamp'].map(lambda x: x.time())
        return _data
    
    def __init__(self, filename: str, devid: str):
        """Class to handle data from an ActiGraph sensors. Each class must be provided with an string (devid).

        Parameters
        ----------
        filename : str
            Name of the filke with the ActiGraph data.
        devid : str
            A unique ID for the device assigned by the user.
        """
        self._filename = filename
        self._id = devid
        
        # Read and organize header string.
        with open(filename, "r") as fh:
            self._head_str = [fh.readline() for _ in range(9)]
        self._head_str[0] = " ".join(self._head_str[0].split(" ")[1:-1])
        
        # Read and organize csv data.
        self._data = ActiGraphData.read_organize_data(self._filename,
                                                      header=10)
        
        # Sampling time of the data.
        self._samplingtime = self._data['TimeStamp'].diff().mode(dropna=True)[0].total_seconds()
        
    @property
    def filename(self):
        return self._filename
    
    @property
    def id(self):
        return self._devid
    
    @property
    def head_str(self):
        return self._head_str
    
    @property
    def data(self):
        return self._data
    
    @property
    def dates(self):
        return self._data['Date'].unique()
    
    @property
    def columns(self):
        return self._data.columns

    @property
    def samplingtime(self):
        return self._samplingtime
    
    def get_data_between_timestamps(self, start: Timestamp, stop: Timestamp) -> DataFrame:
        """Returns a slice of the data between the given timestamps.

        Args:
            start (Timestamp): Start timestamp for slicing the data.
            stop (Timestamp): Stop timestamp for slicing the data.

        Returns:
            DataFrame: Dataframe containing the data between the given
            timestamps.
        """
        assert isinstance(start, Timestamp), "start must be a Timestamp"
        assert isinstance(stop, Timestamp), "stop must be a Timestamp"
        
        _inx = ((self._data['TimeStamp'] >= start)
                * (self._data['TimeStamp'] <= stop))
        return self._data[_inx]
    
    def get_date_time_segments(self, date: datetime.date) -> list[tuple[Timestamp, Timestamp]]:
        """Returns the start and end times of continuous time segments for
        the given date. A time segment is one where successive times points
        are not separated by more then 1 sec.

        Args:
            date (Timestamp.date): Date for which continuous time segments are
            to the identified.

        Returns:
            list[tuple[Timestamp, Timestamp]]: List of tuples with each
            containing two datetime time types. Each tuple indicates the start
            and end times for the continuous time segments found the data. 
        """
        assert isinstance(date, datetime.date),\
            'date should be an datetime date.'
        
        if date not in self.dates:
            return []
        
        return get_continuous_time_segments(
            timeseries=self._data[self._data['Date'] == date]['TimeStamp'],
            deltatime=pandas.Timedelta(self._samplingtime, "sec")
        )
    
    def get_all_time_segments(self) -> list[tuple[Timestamp, Timestamp]]:
        """Returns the start and end times of continuous time segments in the
        entire data. A time segment is one where successive times points
        are not separated by more then 1 sec.

        Returns:
            list[tuple[Timestamp, Timestamp]]: List of tuples with each
            containing two datetime time types. Each tuple indicates the start
            and end times for the continuous time segments found the data.
        """
        return get_continuous_time_segments(
            timeseries=self._data['TimeStamp'],
            deltatime=pandas.Timedelta(self._samplingtime, "sec")
        )

    def __len__(self):
        return len(self._data)
    
    def __repr__(self):
        return f"ActiGraphData(filename='{self._filename}', id='{self._id}')"


def get_continuous_time_segments(timeseries: pandas.core.series.Series,
                                 deltatime: Timedelta) -> list[tuple[Timestamp, Timestamp]]:
    """Returns the start and end times of continuous time segments in the
    given timeseries. A time segment is one where successive timestamps
    are separated by deltatime.

    Args:
        timeseries (pandas.core.series.Series): 1D array of Timestamps from which
        continuous time segments are to be identified.
        deltatime (Timedelta): Difference in timestamps between two successive
        timestamps in a continuous time segment.

    Returns:
        list[tuple[Timestamp, Timestamp]]: List of tuples with each
        containing two datetime time types. Each tuple indicates the start
        and end times for the continuous time segments found the Timestamp
        timeseries.
    """
    pass
    # Compute time differences.
    _tdiff = timeseries.diff()
    _pos = _tdiff.index[_tdiff != deltatime].to_list() + [_tdiff.index[-1]]
    
    return [(timeseries[_strt], timeseries[_end])
            for (_strt, _end) in zip(_pos[:-1], _pos[1:])]
    

def get_common_time_segments(timeseries1: pandas.core.series.Series,
                             timeseries2: pandas.core.series.Series) -> list[tuple[Timestamp, Timestamp]]:
    """Returns the continuous common time segments for the two given timeseries
    of timestamps. deltatime is the difference between two successive timestamps
    in continuous time segment.

    Args:
        timeseries1 (pandas.core.series.Series): Pandas Series of timestamps. 
        timeseries2 (pandas.core.series.Series): Pandas Series of timestamps.
        deltatime (Timedelta): Difference in timestamps between two successive
        timestamps in a continuous time segment.

    Returns:
        list[tuple[Timestamp, Timestamp]]: List of tuples with each
        containing two datetime time types. Each tuple indicates the start
        and end times for the continuous time segments found the Timestamp
        timeseries.
    """
    comm_timeseries = timeseries1[timeseries1.isin(timeseries2)]
    return get_continuous_time_segments(
        timeseries=comm_timeseries,
        deltatime=comm_timeseries.diff().mode(dropna=True)[0]
    )
    
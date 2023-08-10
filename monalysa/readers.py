"""
``readers.py`` is a module for reading data from different wearable sensors 
that are commonly used for movement tracking applications.

The current version supports the following sensor types:

1. `ActiGraph <https://theactigraph.com/>`_ sensor.

----
"""

import pandas
from pandas import DataFrame
from pandas import Timestamp, Timedelta
from datetime import datetime as dt
from datetime import timedelta as td
import datetime
import re


class ActiGraphData(object):
    """Class to handle the activity counts data from an ActiGraph sensor.
    """
    
    @staticmethod
    def shorten_name(name: str) -> str:
        """Shorten the name of the data columns.
        """
        # Short names
        short_names = {
            "Accelerometer X": "AcclX",
            "Accelerometer Y": "AcclY",
            "Accelerometer Z": "AcclZ",
        }
        return short_names[name] if name in short_names else name
    
    @staticmethod
    def read_organize_data(filename, header=10, header_details=None) -> DataFrame:
        """Function to read CSV ActiGraph data file.
        """
        _data = pandas.read_csv(filename, header=header, sep=",")
        _data.columns = [_c.strip() for _c in _data.columns]
        
        # Check if date and time columns
        if "Date" not in _data.columns or "Time" not in _data.columns:
            try:
                deltat = td(seconds=1/header_details['fsamp'])
                _data["TimeStamp"] = header_details['startdatetime'] + _data.index * deltat
            except TypeError:
                print("No sampling frequency information found in the header. Cannot set the timestamp.")
        else:
            # Add a datetime columns
            _data['TimeStamp'] = _data["Date"] + _data['Time']
            _data['TimeStamp'] = _data['TimeStamp'].map(lambda x: dt.strptime(x, "%d/%m/%Y%H:%M:%S"))
            _data['Date'] = _data['TimeStamp'].map(lambda x: x.date())
            _data['Time'] = _data['TimeStamp'].map(lambda x: x.time())
        
        # Get shortened names for the columns
        _data.rename({_c: ActiGraphData.shorten_name(_c) for _c in _data.columns},
                     inplace=True, axis=1)

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
        
        # Header details.
        self._hdetails = self._get_header_details(self._head_str)
        
        # Read and organize csv data.
        self._data = ActiGraphData.read_organize_data(self._filename, header=10,
                                                      header_details=self._hdetails)
        
        # Sampling time of the data.
        if self._hdetails['fsamp'] is not None:
            self._samplingtime = 1/self._hdetails['fsamp']
        elif 'TimeStamp' in self._data.columns:
            self._samplingtime = self._data['TimeStamp'].diff().mode(dropna=True)[0].total_seconds()
        else:
            self._samplingtime = None
        
    @property
    def filename(self):
        return self._filename
    
    @property
    def id(self):
        return self._id
    
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
    
    def _get_header_details(self, header_str: str) -> dict:
        """Get the details of the file from the doc string.

        Parameters
        ----------
        header_str : str
            Header string read from the CSV file.

        Returns
        -------
        dict
            Dictionary contians the details of the file: Sampling frequency (if available),
            starting datetime.
        """
        _details = {}
        srch = re.compile(r'^.*\s([0-9]*)\sHz\s.*$')
        if srch.match(header_str[0]) is not None:
            _srchout = srch.match(header_str[0]).groups()
            _details['fsamp'] = int(_srchout[0])
        else:
            _details['fsamp'] = None
        
        # Find start datetime
        _strtime = [_str.split()[-1] for _str in header_str if 'Start Time' in _str][0]
        _strdate = [_str.split()[-1] for _str in header_str if 'Start Date' in _str][0]
        
        # Start datetime
        _details['startdatetime'] = dt.strptime(_strdate + _strtime, "%d/%m/%Y%H:%M:%S")

        return _details
    
    def _get_sampling_freq_from_header(self, header_str: str) -> float or None:
        """Returns the sampling frequency of the data from the header string.
        """
        return float(self._head_str[1].split(" ")[-1])
    
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
    
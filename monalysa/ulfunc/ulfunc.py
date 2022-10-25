"""
ulfunc.py contains functions and classes for implementing different measures
for quantifying upper-limb functioning. 
"""

import numpy as np
from scipy import signal
from datetime import datetime as dt


class ULUse(object):
    """Class implementing different UL use measures as static functions.
    """
    @staticmethod
    def from_activity_counts1(actcounts: np.array,
                              threshold: float) -> np.array:
        """A single threshold based algorithm for computing UL use
        from activity counts.

        Args:
            actcounts (np.array): 1D numpy array containing the activity counts
            time series.
            threshold (float): Threshold for generating the binary UL use
            output time series.

        Returns:
            np.array: 1D numpy array of the UL use signal, which is a binary
            signal indicating the presence or absence of a "functional"
            movement any time instant.
        """
        assert len(actcounts) > 0, "actcounts cannot be a of zero length."
        assert min(actcounts) >= 0., "Activity count cannot be negative."
        
        return  1.0 * np.array(np.array(actcounts) >= threshold)
    
    @staticmethod
    def from_activity_counts2(actcounts: np.array,
                              threshold0: float,
                              threshold1: float) -> np.array:
        """A hysteresis based based algorithm for computing UL use
        from activity counts.
        Note: Since this method requires information about the past value of
        UL use, you must ensure that the activtiy counts input is from a
        continuous time segment.  

        Args:
            actcounts (np.array): 1D numpy array containing the activity counts
            time series.
            threshold0 (float): Threshold below which UL use signal is 0.
            threshold1 (float): Threshold above which UL use signal is 1.

        Returns:
            np.array: 1D numpy array of the UL use signal, which is a binary
            signal indicating the presence or absence of a "functional"
            movement any time instant.
        """
        assert len(actcounts) > 0, "actcounts cannot be a of zero length."
        assert min(actcounts) >= 0., "Activity count cannot be negative."
        assert threshold0 <= threshold1, "threshold0 must be smaller than threshold1."
        
        if threshold0 == threshold1:
            print("Both thresholds are the same. Using from_activity_counts1 function to compute UL use.")
            return ULUse.from_activity_counts1(actcounts, threshold0)

        _uluse = np.zeros(len(actcounts))
        _uluse[actcounts >= threshold1] = 1
        
        # Indices in the intermediate region where the activity count is
        # less than threshold1 but greater than threshold0.
        _temp = np.where((actcounts >= threshold0)
                         * (actcounts < threshold1))[0]
        # Check if the very first point is in the intermediate region.
        for i in _temp:
            _uluse[i] = _uluse[i-1] if i > 0  else 0
        
        return _uluse


# def average_uluse(uluse: np.array, dur: float, sample_t: float) -> np.array:
#     """Computes the average upper-limb use from the given UL use signal. The
#     current version only supports causal averaging.

#     Args:
#         uluse (np.array): 1D numpy array of the UL use (binary) signal whose
#         average is to be computed.
#         dur (float): Duration in seconds over which the UL use signal is to be
#         averaged.
#         sample_t (float): Sampling time of the uluse signal.

#     Returns:
#         np.array: 1D numpy array of the averaged UL use signal.
#     """
#     assert ((uluse == 0) + (uluse == 1)).all(),\
#         "uluse must be a binary signal."
#     assert dur > 0, "dur (avaraging duration) must be a positive number."
#     assert sample_t > 0, "dt (sampling time) must be a positive number."
    
#     N = int(dur / sample_t)
#     return signal.lfilter(b=np.ones(N), a=np.array([N]), x=uluse)


# def average_intuse(ulint: np.array, uluse: np.array, dur: float, sample_t: float) -> np.array:
#     """Computes the average upper-limb intensity of use from the given
#     intensity and UL use signals. The current version only supports causal
#     averaging.

#     Args:
#         ulint (np.array): 1D numpy array of the UL intensity signal whose
#         average is to be computed.
#         uluse (np.array): 1D numpy array of the UL use (binary) signal.
#         dur (float): Duration in seconds over which the UL internsity signal
#         is to be averaged.
#         sample_t (float): Sampling time of the ulint and uluse signal.

#     Returns:
#         np.array: 1D numpy array of the averaged UL use signal.
#     """
#     assert np.shape(ulint) == np.shape(uluse),\
#         "ulint and uluse must have the same shape."
#     assert min(ulint) >= 0., "ulint signal cannot be negative."
#     assert ((uluse == 0) + (uluse == 1)).all(),\
#         "uluse must be a binary signal."
#     assert dur > 0, "dur (avaraging duration) must be a positive number."
#     assert sample_t > 0, "dt (sampling time) must be a positive number."
    
#     N = int(dur / sample_t)
#     _avgint = signal.lfilter(b=np.ones(N), a=np.array([N]), x=ulint)
#     _avguse = signal.lfilter(b=np.ones(N), a=np.array([N]), x=uluse)
#     return np.array([
#         _ai / _au if _au > 0 else 0
#         for _ai, _au in zip(_avgint, _avguse)
#     ])


def average_ulactivity(intsig: np.array, windur: float, winshift: float,
                       sample_t: float) -> np.array:
    """Computes the average upper-limb activity of use from the given
    intensity and UL use signals. The current version only supports causal
    averaging.

    Args:
        intsig (np.array): 1D numpy array of the instantaneous UL intensity
        signal whose average is to be computed.
        windur (float): Duration in seconds over which the UL use signal is to
        be averaged.
        winshift (float): Time shift between two consecutive averaging windows.
        sample_t (float): Sampling time of the intsig signal.

    Returns:
        np.array: 1D numpy array of the average upper-limb activity.
    """
    assert np.nanmin(intsig) >= 0., "intsig signal cannot be negative."
    assert windur > 0, "windur (avaraging window duration) must be a positive number."
    assert winshift > 0, "winshift (time shift between consecutive windows) must be a positive number."
    assert sample_t > 0, "sample_t (sampling time) must be a positive number."
    
    n_win = int(windur / sample_t)
    n_shift = int(windur / sample_t)
    ulact = signal.lfilter(b=np.ones(n_win), a=np.array([n_win]), x=intsig) 
    return (np.arange(0, len(intsig), n_shift), ulact[::n_shift])


def Hq(aua: np.array, q: float) -> float:
    """Computes the over  upper-limb activity using the average upper-limb
    activity time series.

    Args:
        aua (np.array): 1D numpy array of the average upper-limb activity.
        q (float): Percentile to be used for computing the overall upper-limb
        activity. This value must be between 0 and 100.

    Returns:
        float: Hq computed from the given average upper-limb activity
        time series.
    """
    if np.all(np.isnan(aua)):
        return np.NaN
    
    assert np.nanmin(aua) >= 0, "Average upper-limb activity must be non-negative."
    assert (q >= 0) and (q <= 100), "q (percentile) must be between 0 and 100."

    return np.nanpercentile(aua, q) if not np.isnan(np.nanmin(aua)) else np.nan


def Rq(domnaff: np.array, ndomaff: np.array, q: float) -> tuple[float, float]:
    """Computes the relative upper-limb use from the data given for the two 
    upper-limbs.

    Args:
        domnaff (np.array): 1D numpy array of data from the dominant or
        non-affected upper limb.
        ndomaff (np.array): 1D numpy array of data from the non-dominant or
        affected upper limb.
        q (float): Percentile to be used for computing the realtive upper-limb
        use. This value must be between 0 and 100.

    Returns:
        tuple[float, float]: The first value of the tuple is Rq which takes a
        value between 0 and 1, and the second value is -1, 0, or +1, depending
        which upper-limb is used more than the other.
    """
    if np.all(np.isnan(domnaff)) or np.all(np.isnan(ndomaff)):
        return np.NaN, np.NaN
    
    assert np.nanmin(domnaff) >= 0, "domnaff must be non-negative."
    assert np.nanmin(ndomaff) >= 0, "ndomaff must be non-negative."
    assert len(domnaff) == len(ndomaff), "Data for the two upper-limbs must be equal in length."
    assert (q >= 0) and (q <= 100), "q (percentile) must be between 0 and 100."
    
    _q1 = np.nanpercentile(domnaff, q)
    _q2 = np.nanpercentile(ndomaff, q)
    _q12 = np.nanpercentile(domnaff * ndomaff, q)

    if (_q1 == 0 and _q2 == 0):
        return np.NaN, np.NaN
    
    return (_q12 / np.max([np.square(_q1), np.square(_q2)]),
            0 if _q1 == _q2 else np.sign(_q1 - _q2))
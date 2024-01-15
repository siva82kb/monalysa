"""
``measures.py`` contains functions and classes for implementing different measures for quantifying upper-limb functioning. 

----
"""

from scipy import signal
import numpy as np


def Hq(aua: np.array, q: float) -> float:
    """Computes the overall upper-limb activity using the average upper-limb
    activity time series.

    Args:
        aua (np.array): 1D numpy array of the average upper-limb activity.
        q (float): Percentile to be used for computing the overall upper-limb activity. This value must be between 0 and 100.

    Returns:
        float: Hq computed from the given average upper-limb activity time series.
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
        domnaff (np.array): 1D numpy array of data from the dominant or non-affected upper limb.
        ndomaff (np.array): 1D numpy array of data from the non-dominant or affected upper limb.
        q (float): Percentile to be used for computing the relative upper-limb use. This value must be between 0 and 100.

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


def instantaneous_latindex(domnaff: np.array, ndomaff: np.array) -> tuple[np.array, np.array]:
    """Computes the instantaneous laterality index using the two given signals 
    corresponding to the two arms. This can be computed with either 
    instantaneous use or intensity signals. Both signals must be of the same 
    type, i.e. both must be use signals or both must be intensity signals. 
    Mixing signals will produce results that are not interpretable.

    Parameters
    ----------
    domnaff : np.array
        Instantaneous use or intensity signal for the dominant or the 
        unaffected upper-limb.
    ndomaff : np.array
        Instantaneous use or intensity signal for the non-dominant or the 
        affected upper-limb.

    Returns
    -------
    tuple[np.array, np.array]
        A tuple of 1D numpy arrays. The first 1D  array is the list of time indices of the computed instantaneous laterality index signal. The second 1D array is the instantaneous laterality index signal.
    """
    if np.all(np.isnan(domnaff)) or np.all(np.isnan(ndomaff)):
        return np.ones(len(domnaff)) * np.NaN
    
    assert len(domnaff) == len(ndomaff), "Both the dominant and non-dominant signals must be of the same length."
    assert np.nanmin(domnaff) >= 0, "The input dominant/affected limb signal must be non-negative."
    assert np.nanmin(ndomaff) >= 0, "The input non-dominant/unaffected limb signal must be non-negative."
    
    _sum = np.array(ndomaff) + np.array(domnaff)
    _diff = np.array(domnaff) - np.array(ndomaff)
    _diff[_sum == 0] = np.NaN
    _diff[_sum != 0] = _diff[_sum != 0] / _sum[_sum != 0]
    return np.arange(0, len(_diff)), _diff


def average_latindex(latinx_inst: np.array, windur: float, winshift: float,
                     fs: float) -> tuple[np.array, np.array]:
    """Compute the average of the instantaneous laterality index signal.

    Parameters
    ----------
    latinx_inst : np.array
        The instantaneous laterality index signal.
    windur : float
        Duration in seconds over which the UL use signal is to be averaged.
    winshift : float
        Time shift between two consecutive averaging windows.
    sample_t : float
        Sampling frequency of the usesig signal.

    Returns
    -------
    tuple[np.array, np.array]
        A tuple of 1D numpy arrays. The first 1D  array is the list of time indices of the computed average laterality index signal. The second 1D array is the average laterality index signal.
    """
    
    assert windur > 0, "windur (averaging window duration) must be a positive number."
    assert winshift > 0, "winshift (time shift between consecutive windows) must be a positive number."
    assert fs > 0, "fs (sampling frequency) must be a positive number."
    assert np.all(np.any(np.array([np.abs(latinx_inst) <= 1,
                                   np.isnan(latinx_inst)]),
                         axis=0)), "Laterality index signal cannot be less than -1 or greater than +1. Nan is also allowed."
    
    n_win = int(windur * fs)
    n_shift = int(windur * fs)
    avg_latinx = signal.lfilter(b=np.ones(n_win), a=np.array([n_win]), x=latinx_inst) 
    return (np.arange(0, len(latinx_inst), n_shift), avg_latinx[::n_shift])
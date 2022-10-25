"""
uluse.py is a module containing different class, and functions for quanitfying
the UL use construct.

Author: Sivakumar Balasubramanian
Date: 17 Oct 2022
Email: siva82kb@gmail.com 
"""

import numpy as np
from scipy import signal
from datetime import datetime as dt

from .. import misc


def from_vector_magnitude1(vecmag: np.array,
                           threshold: float) -> tuple[np.array, np.array]:
    """A single threshold based algorithm for computing UL use
    from activity counts.

    Args:
        vecmag (np.array): 1D numpy array containing the activity counts time series.
        threshold (float): Threshold for generating the binary UL use output time series.

    Returns:
        tuple[np.array, np.array]: A tuple of 1D numpy arrays. The first 1D 
        array is the list of time indices of the computed UL use signal. The 
        second ID array is the UL use signal, which is a binary
        signal indicating the presence or absence of a "functional"
        movement any time instant.
    """
    assert len(vecmag) > 0, "vecmag cannot be a of zero length."
    assert np.nanmin(vecmag) >= 0., "Activity count cannot be negative."
    
    _use = 1.0 * (vecmag >= threshold)
    _use[np.isnan(vecmag)] = np.nan
    return  (np.arange(len(vecmag)), _use)


def from_vector_magnitude2(vecmag: np.array, threshold0: float,
                           threshold1: float) -> tuple[np.array, np.array]:
    """A hysteresis based based algorithm for computing UL use
    from activity counts.
    Note: Since this method requires information about the past value of
    UL use, you must ensure that the activtiy counts input is from a
    continuous time segment.  

    Args:
        vecmag (np.array): 1D numpy array containing the activity counts time series.
        threshold0 (float): Threshold below which UL use signal is 0.
        threshold1 (float): Threshold above which UL use signal is 1.

    Returns:
        tuple[np.array, np.array]: A tuple of 1D numpy arrays. The first 1D 
        array is the list of time indices of the computed UL use signal. The 
        second ID array is the UL use signal, which is a binary
        signal indicating the presence or absence of a "functional"
        movement any time instant.
    """
    assert len(vecmag) > 0, "vecmag cannot be a of zero length."
    assert np.nanmin(vecmag) >= 0., "Activity count cannot be negative."
    assert threshold0 <= threshold1, "threshold0 must be smaller than threshold1."
    
    if threshold0 == threshold1:
        print("Both thresholds are the same. Using from_vector_magnitude1 function to compute UL use.")
        return from_vector_magnitude1(vecmag, threshold0)

    vecmag = np.array(vecmag)
    _uluse = np.zeros(len(vecmag))
    _uluse[vecmag >= threshold1] = 1
    _uluse[np.isnan(vecmag)] = np.nan
    
    # Indices in the intermediate region where the activity count is
    # less than threshold1 but greater than threshold0.
    _temp = np.where((vecmag >= threshold0)
                     * (vecmag < threshold1))[0]
    for i in _temp:
        if np.isnan(_uluse[i - 1]):
            _uluse[i] = 0
        else:
            _uluse[i] = _uluse[i-1] if i > 0  else 0
    
    return (np.arange(len(_uluse)), _uluse)


def average_uluse(usesig: np.array, windur: float, winshift: float,
                  sample_t: float) -> tuple[np.array, np.array]:
    """Computes the average upper-limb use from the given UL use signal. The
    current version only supports causal averaging.

    Args:
        usesig (np.array): 1D numpy array of the UL use (binary) signal whose
        average is to be computed.
        windur (float): Duration in seconds over which the UL use signal is to
        be averaged.
        winshift (float): Time shift between two consecutive averaging windows.
        sample_t (float): Sampling time of the usesig signal.

    Returns:
        tuple[np.array, np.array]: A tuple of 1D numpy arrays. The first 1D 
        array is the list of time indices of the computed avarge UL use signal. 
        The second ID array is the avarage UL use use signal.
    """
    assert windur > 0, "windur (avaraging window duration) must be a positive number."
    assert winshift > 0, "winshift (time shift between consecutive windows) must be a positive number."
    assert sample_t > 0, "sample_t (sampling time) must be a positive number."
    assert misc.is_binary_signal(usesig, allownan=True), "Use signal must be a binary signal."
    
    n_win = int(windur / sample_t)
    n_shift = int(windur / sample_t)
    avguse = signal.lfilter(b=np.ones(n_win), a=np.array([n_win]), x=usesig) 
    return (np.arange(0, len(usesig), n_shift), avguse[::n_shift])

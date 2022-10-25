"""
ulint.py is a module containing different class, and functions for quanitfying
the UL intensity construct.

Author: Sivakumar Balasubramanian
Date: 17 Oct 2022
Email: siva82kb@gmail.com 
"""

import numpy as np
from scipy import signal
from datetime import datetime as dt

from .. import misc


def from_vector_magnitude(vecmag: np.array, usesig: np.array,
                          nsample: int) -> tuple[np.array, np.array]:
    """Computes UL intensity from the vector magnitude values from the 
    Actigraph sensor.

    Parameters
    ----------
    vecmag : np.array
        1D numpy array containing the activity counts time series.
    usesig : np.array
        1D numpy array of the UL use binary signal.
    nsample : int
        The downsampling number for computing the instantaneous  UL intensity of use. This number must be equal to the ratio of the  sampling rate of the raw data (vecmag) and the uluse data. This means len(vecmag[::nsample]) == len(usesig).

    Returns
    -------
    tuple[np.array, np.array]
        A tuple of 1D numpy arrays. The first 1D array is the list of time indices of the computed UL use signal. The second ID array is the UL use signal, which is a binary
        signal indicating the presence or absence of a "functional" movement any time instant.
    """
    
    assert len(vecmag) > 0, "vecmag cannot be a of zero length."
    assert np.nanmin(vecmag) >= 0., "Vector magnitude cannot be negative."
    assert misc.is_binary_signal(usesig, allownan=True), "Use signal must be a binary signal."
    assert len(vecmag[::nsample]) == len(usesig), "The lengths of vecmag and usesig are not compatible."
    
    return (np.arange(0, len(vecmag), nsample), vecmag[::nsample] * usesig)


def average_intuse(intsig: np.array, usesig: np.array, windur: float,
                   winshift: float, sample_t: float) -> tuple[np.array, np.array]:
    """Computes the average upper-limb intensity of use from the given intensity and UL use signals. The current version only supports causal averaging.

    Parameters
    ----------
    intsig : np.array
        1D numpy array of the UL intensity signal whose average is to be computed.
    usesig : np.array
        1D numpy array of the UL use (binary) signal.
    windur : float
        Duration in seconds over which the UL internsity signal is to be averaged.
    winshift : float
        Time gap between two consecutive window locations.
    sample_t : float
        Sampling time of the intsig and usesig signal.

    Returns
    -------
    tuple[np.array, np.array]
        A tuple of 1D numpy arrays. The first 1D  array is the list of time indices of the computed avarge UL intensity of use signal. The second ID array is the average UL intensity of use signal.
    """
    
    assert np.shape(intsig) == np.shape(usesig), "intsig and usesig must have the same shape."
    assert np.nanmin(intsig) >= 0., "intsig signal cannot be negative."
    assert windur > 0, "windur (avaraging window duration) must be a positive number."
    assert winshift > 0, "winshift (time shift between consecutive windows) must be a positive number."
    assert sample_t > 0, "sample_t (sampling time) must be a positive number."
    assert np.all(np.any(np.array([np.array(intsig) >= 0,
                                   np.isnan(intsig)]), axis=0)), "Use signal must be a binary signal."
    
    n_win = int(windur / sample_t)
    n_shift = int(windur / sample_t)
    _avgint = signal.lfilter(b=np.ones(n_win), a=np.array([n_win]), x=intsig)
    _avguse = signal.lfilter(b=np.ones(n_win), a=np.array([n_win]), x=usesig)
    _avgintuse = np.array([_ai / _au if _au > 0
                           else np.nan if np.isnan(_au)
                           else 0
                           for _ai, _au in zip(_avgint, _avguse)])
    return (np.arange(0, len(intsig), n_shift), _avgintuse[::n_shift])

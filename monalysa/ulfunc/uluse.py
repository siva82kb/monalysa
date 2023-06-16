"""
``uluse.py`` is a module containing different classes, and functions for quanitfying
the UL use construct - instantaneous and average use. 

The current version of the module contains the following instantaneous UL use algorithms:

1. Vector magnitude from the Actigraph sensor (with and without hysterisis)
2. GMAC (Gross Movement + Activity Countys)

----
"""

import numpy as np
from scipy import signal
from datetime import datetime as dt
from scipy import signal

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
    return (np.arange(len(vecmag)), _use)


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
            _uluse[i] = _uluse[i - 1] if i > 0 else 0

    return (np.arange(len(_uluse)), _uluse)


def from_gmac(acc_forearm: np.array, acc_ortho1: np.array, acc_ortho2: np.array,
              sampfreq: int, pitch_threshold: int=30,
              counts_threshold: int=0) -> tuple[np.array, np.array]:
    """
    Computes UL use using the GMAC algorithm with pitch and counts estimated only from acceleration.
    
    Args:
        acc_forearm (np.array):  1D numpy array containing acceleration along the length of the forearm.
        acc_ortho1 (np.array): 1D numpy array containing acceleration along one of the orthogonal axis to the forearm.
        acc_ortho2 (np.array): 1D numpy array containing acceleration along the other orthogonal axis to the forearm.
        sampfreq (int): Sampling frequency of acceleration data.
        pitch_threshold (int): Pitch between +/- pitch_threshold are considered functional, default=30 (Leuenberger et al. 2017).
        counts_threshold (int): Counts greater than counts_threshold are considered functional, default=0 (optimized for youden index).

    Returns:
        tuple[np.array, np.array]: A tuple of 1D numpy arrays. The first 1D
        array is the list of time indices of the computed UL use signal. The
        second ID array is the UL use signal, which is a binary
        signal indicating the presence or absence of a "functional"
        movement any time instant.
    """
    assert len(acc_forearm) == len(acc_ortho1), "acc_forearm, acc_ortho1 and acc_ortho2 must be of equal length"
    assert len(acc_ortho1) == len(acc_ortho2), "acc_forearm, acc_ortho1 and acc_ortho2 must be of equal length"
    assert sampfreq > 0, "sampfreq must be a positive integer"

    # 1 second moving average filter
    acc_forearm = np.append(np.ones(sampfreq - 1) * acc_forearm[0], acc_forearm)  # padded at the beginning with the first value
    acc_forearm = np.convolve(acc_forearm, np.ones(sampfreq), 'valid') / sampfreq

    acc_forearm[acc_forearm < -1] = -1
    acc_forearm[acc_forearm > 1] = 1
    pitch_hat = -np.rad2deg(np.arccos(acc_forearm)) + 90

    hpf_cutoff = 1  # 1Hz high pass filter
    b, a = signal.butter(2, hpf_cutoff / (2 * sampfreq), 'high')
    acc_forearm_filt = signal.filtfilt(b, a, acc_forearm)
    acc_ortho1_filt = signal.filtfilt(b, a, acc_ortho1)
    acc_ortho2_filt = signal.filtfilt(b, a, acc_ortho2)

    deadband_threshold = 0.068  # Brond et al. 2017
    acc_forearm_filt[np.abs(acc_forearm_filt) < deadband_threshold] = 0
    acc_ortho1_filt[np.abs(acc_ortho1_filt) < deadband_threshold] = 0
    acc_ortho2_filt[np.abs(acc_ortho2_filt) < deadband_threshold] = 0

    amag = [np.linalg.norm(x) for x in np.column_stack((acc_forearm_filt, acc_ortho1_filt, acc_ortho2_filt))]
    amag = [sum(amag[i:i + sampfreq]) for i in range(0, len(amag), sampfreq)]

    # 5 second moving average filter
    window = 5  # Bailey et al. 2014
    amag = np.append(np.ones(window - 1) * amag[0], amag)
    amag = np.convolve(amag, np.ones(window), 'valid') / window

    _uluse = [1 if np.abs(pitch) < pitch_threshold and count > counts_threshold else 0
                for pitch, count in zip(pitch_hat[0:len(pitch_hat):sampfreq], amag)]
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
    n_shift = int(winshift / sample_t)
    avguse = signal.lfilter(b=np.ones(n_win), a=np.array([n_win]), x=usesig)
    return (np.arange(0, len(usesig), n_shift), avguse[::n_shift])

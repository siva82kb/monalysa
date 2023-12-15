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
from scipy import signal

from .. import misc


def from_vector_magnitude1(vecmag: np.array,
                           threshold: float) -> tuple[np.array, np.array]:
    """A single threshold based algorithm for computing UL use
    from activity counts.

    Parameters
    ----------
    vecmag : np.array
        1D numpy array containing the activity counts time series.
    threshold : float
        Threshold for generating the binary UL use output time series.

    Returns
    -------
    tuple[np.array, np.array]
        A tuple of 1D numpy arrays. The first 1D array is the list of time 
        indices of the computed UL use signal. The second ID array is the UL 
        use signal, which is a binary signal indicating the presence or absence 
        of a "functional" movement any time instant.
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

    Parameters
    ----------
    vecmag : np.array
        1D numpy array containing the activity counts time series.
    threshold0 : float
        Threshold below which UL use signal is 0.
    threshold1 : float
        Threshold above which UL use signal is 1.

    Returns
    -------
    tuple[np.array, np.array]
        A tuple of 1D numpy arrays. The first 1D array is the list of time 
        indices of the computed UL use signal. The second ID array is the UL 
        use signal, which is a binary signal indicating the presence or absence 
        of a "functional" movement any time instant.
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


def estimate_accl_pitch(accl: np.array, farm_inx: int, elb_to_farm: bool,
                        nwin: int) -> np.array:
    """
    Estimates the pitch angle of the forearm from the accelerometer data.

    Parameters
    ----------
    accl : np.array
        2D numpy array containing the acceleration data with columns 
        corresponding to different components (at most 3), and rows 
        corresponding to sampling instants.
    farm_inx : int
        Index of the forearm component of the acceleration data. Must be an integer between 0 and the number of columns in accl.
    elb_to_farm: bool
        Indicates if the axis points from the eblow to forearm, or the other way around.
    nwin : int
        Number of samples to use for moving averaging. Must be a positive integer.
    
    Returns
    -------
    np.array
        1D numpy array containing the pitch angle of the forearm estiamted from 
        the accelerometer data.
    """
    assert len(accl.shape) == 2, "accl must be a 2D numpy array."
    assert accl.shape[1] <= 3, "accl must have at most 3 columns."
    assert farm_inx >= 0 and farm_inx < accl.shape[1], "farm_inx must be an integer between 0 and the number of columns in the accelerometer data."
    assert type(elb_to_farm) == bool, "elb_to_farm must be a boolean."
    assert nwin > 0, "nwin must be a positive integer."

    # Moving averaging using the causal filter
    acclf = signal.lfilter(np.ones(nwin) / nwin, 1, accl, axis=0) if nwin > 1 else accl
    # Compute the norm of the acceleration vector
    acclfn = acclf / np.linalg.norm(acclf, axis=1, keepdims=True)
    _sign = 1 if elb_to_farm else -1
    return _sign * np.rad2deg(np.arcsin(acclfn[:, farm_inx]))


def estimate_accl_mag(accl: np.array, fs: float, fc: float, nc: int,
                      n_am: int) -> np.array:
    """
    Computes the magnitude of the accelerometer signal.

    Parameters
    ----------
    accl : np.array
        2D numpy array containing the acceleration data with columns 
        corresponding to different components (at most 3), and rows 
        corresponding to sampling instants.
    fs : float
        Sampling frequency of the acceleration data.
    fc : float
        Cutoff frequency for the highpass filter used for filtering the acceleration data.
    nc : int
        Order of the highpass filter used for filtering the acceleration data.
    n_am : int
        Number of samples to use for moving averaging. Must be a positive integer.
    
    Returns
    -------
    np.array
        1D numpy array containing the magnitude of the acceleration data.
    """
    assert len(accl.shape) == 2, "accl must be a 2D numpy array."
    assert accl.shape[1] <= 3, "accl must have at most 3 columns."
    assert fs > 0, "fs must be a positive number."
    assert fc > 0, "fc must be a positive number."
    assert nc > 0, "nc must be a positive integer."
    assert n_am > 0, "n_am must be a positive integer."
    
    # Highpass filter the acceleration data.
    sos = signal.butter(nc, fc, btype='highpass', fs=fs, output='sos')
    accl_filt = np.array([signal.sosfilt(sos, accl[:, 0]),
                          signal.sosfilt(sos, accl[:, 1]),
                          signal.sosfilt(sos, accl[:, 2])]).T
    
    # Acceleration magnitude    
    amag = np.linalg.norm(accl_filt, axis=1)
    
    # Return the moving averageed amag
    return signal.lfilter(np.ones(n_am) / n_am, 1, amag, axis=0)


def detector_with_hystersis(x: np.array, th: float, th_band: float) -> np.array:
    """
    Implements a binary detector with hystersis.

    Parameters
    ----------
    x : np.array
        1D numpy array containing the input signal.
    th : float
        Upper threshold for the detector to output 1.
    th_band : float
        Hystersis band for the detector. The output of the detector will be 1
        as long as the input signal is greater than or equal to (th - th_band).
        If the input signal is less than (th - th_band), the output of the
        detector will be 0.
    
    Returns
    -------
    np.array
        1D numpy array containing the output of the detector.
    """
    y= np.zeros(len(x))
    for i in range(1, len(y)):
        if y[i-1] == 0:
            y[i] = 1 * (x[i] > th)
        else:
            y[i] = 1 * (x[i] >= (th - th_band))
    return y


def from_gmac(accl: np.array, fs: float, 
              accl_farm_inx: int, elb_to_farm: bool,
              np: int, fc: float, nc: int, nam: int,
              p_th: float, p_th_band: float,
              am_th: float, am_th_band: float) -> np.array:
    """
    Computes UL use using the GMAC algorithm with pitch and acceleration magnitude estimated only from acceleration.

    Parameters
    ----------
    accl : np.array
        2D numpy array containing the acceleration data with columns corresponding to different components (at most 3), and rows 
        corresponding to sampling instants.
    fs : float
        Sampling frequency of the acceleration data. Must be a positive number.
    accl_farm_inx : int
        Index of the forearm component of the acceleration data. Must be an integer between 0 and  and the number of columns in accl.
    elb_to_farm: bool
        Indicates if the axis points from the eblow to forearm, or the other way around.
    np : int
        Number of samples to use for moving averaging. Must be a positive integer.
    fc : float
        Cutoff frequency for the highpass filter used for filtering the acceleration data. Must be a positive number.
    nc : int
        Order of the highpass filter used for filtering the acceleration data. Must be a positive integer.
    nam : int
        Number of samples to use for moving averaging. Must be a positive integer.
    p_th : float
        Upper threshold for the pitch angle.
    p_th_band : float
        Hystersis band for the pitch angle.
    am_th : float
        Upper threshold for the acceleration magnitude.
    am_th_band : float
        Hystersis band for the acceleration magnitude.

    Returns
    -------
    np.array
        Returns a 2D array with 3 columns and N rows. The first column corresponds
        to the pitch angle, the second column corresponds to the acceleration
        magnitude, and the third column corresponds to the GMAC output. 
    """
    # Estimate pitch and acceleration magnitude
    pitch = estimate_accl_pitch(accl, accl_farm_inx, elb_to_farm, np)
    accl_mag = estimate_accl_mag(accl, fs, fc=fc, nc=nc, n_am=nam)
    
    # Compute GMAC
    _pout = detector_with_hystersis(pitch, th=p_th, th_band=p_th_band)
    _amout = detector_with_hystersis(accl_mag, th=am_th, th_band=am_th_band)
    return np.array([pitch, accl_mag, _pout * _amout])


def average_uluse(usesig: np.array, windur: float, winshift: float,
                  sample_t: float) -> tuple[np.array, np.array]:
    """Computes the average upper-limb use from the given UL use signal. The
    current version only supports causal averaging.

    Parameters
    ----------
    usesig : np.array
        1D numpy array of the UL use (binary) signal whose average is to be computed.
    windur : float
        Duration in seconds over which the UL use signal is to be averaged.
    winshift : float
        Time shift between two consecutive averaging windows.
    sample_t : float
        Sampling time of the usesig signal.

    Returns
    -------
    tuple[np.array, np.array]
        A tuple of 1D numpy arrays. The first 1D array is the list of time 
        indices of the computed avarge UL use signal. The second ID array is 
        the avarage UL use use signal.
    """
    assert windur > 0, "windur (avaraging window duration) must be a positive number."
    assert winshift > 0, "winshift (time shift between consecutive windows) must be a positive number."
    assert sample_t > 0, "sample_t (sampling time) must be a positive number."
    assert misc.is_binary_signal(usesig, allownan=True), "Use signal must be a binary signal."

    n_win = int(windur / sample_t)
    n_shift = int(winshift / sample_t)
    avguse = signal.lfilter(b=np.ones(n_win), a=np.array([n_win]), x=usesig)
    return (np.arange(0, len(usesig), n_shift), avguse[::n_shift])

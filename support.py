"""
support.py is a module that provides a set of supporitng functions used by 
other modules in the monalysa library.

Author: Sivakumar Balasubramanian
Date: 17 Oct 2022
Email: siva82kb@gmail.com
"""

import numpy as np
import pandas as pd


def is_binary_signal(sig: np.array, allownan=False) -> bool:
    """Indicates if the given input signal is a binary signal. Nan values can
    be allowed.

    Args:
        sig (np.array): Input signal that is to be checked if it is a binary
        signal.
        allownan (bool): Boolean to include if nans are to be allowed in the 
        signal when testing it.

    Returns:
        bool: True if the signal is binary, else its False.
    """
    _test = [sig != 0, sig != 1]
    _test += [np.isnan(sig).tolist()] if allownan else []
    return np.all(np.any(_test, axis=0))

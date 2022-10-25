"""
misc.py is a module containing a set of additional useful functions for use by 
other modules in monalysa.

Author: Sivakumar Balasubramanian
Email: siva82kb@gmail.com
Date: 25 Oct 2022 
"""

from typing import Union
import numpy as np


def is_integer_num(n: Union[int, float]) -> bool:
    """Checks if the given number is an integer.

    Parameters
    ----------
    n : Union[int, float]
        The number that is to be checked if it is an
        integer.

    Returns
    -------
    bool
        Bool indicating if the number is an integer. True if n is an
        integer, else its False
    """
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False


def is_binary_signal(sig: np.array, allownan=False) -> bool:
    """Indicates if the given input signal is a binary signal. Nan values can be allowed.

    Parameters
    ----------
    sig : np.array
        Input signal that is to be checked if it is a binary signal.
    allownan : bool, optional
        Boolean to include if nans are to be allowed in the  signal when testing it., by default False

    Returns
    -------
    bool
        True if the signal is binary, else its False.
    """
    _test = [sig == 0, sig == 1]
    _test += [np.isnan(sig).tolist()] if allownan else []
    return np.all(np.any(_test, axis=0))
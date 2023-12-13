"""
misc.py is a module containing a set of useful functions monalysa library.

----
"""

from typing import Union
import numpy as np


def is_integer_num(num: Union[int, float]) -> bool:
    """Checks if the given number is an integer.

    Parameters
    ----------
    num : Union[int, float]
          The number that is to be checked if it is an
          integer.

    Returns
    -------
    bool
        Bool indicating if the number is an integer. True if n is an
        integer, else its False
    """
    if isinstance(num, int):
        return True
    if isinstance(num, float):
        return num.is_integer()
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


def gram_schmidt_orthogonalize(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Perform the Gram-Schmidt orthogonalization.

    Parameters
    ----------
    x : np.ndarray
        2D array of number corresponding to the x vector. The columns are the 
        different components, while the rows are different x vectors.
    y : np.ndarray
        2D array of number corresponding to the y vector. The columns are the 
        different components, while the rows are different y vectors.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        Returns the GS orthogonalized (x_normn, y_norm) vectors, with the rows corresponding 
        to the different orthogonalized vectors, and the columsn corresponding 
        to the different components.
        The norm of the rows of x_norm and y_norm will 1. The dot product of 
        the rows of the x_norm nad y_norm will be 0.
    """
    assert type(x) == np.ndarray, "x must be an numpy ndarray."
    assert type(y) == np.ndarray, "x must be an numpy ndarray."
    assert len(x.shape) == 2, "x must be anb 2D numpy array."
    assert len(y.shape) == 2, "x must be anb 2D numpy array."
    assert x.shape == y.shape, "x and y must have the same shape"
    
    _xn = x / np.linalg.norm(x, axis=1, keepdims=True)
    _yx = np.sum(y * _xn, axis=1, keepdims=True)
    _dy = y - _xn * _yx
    _yn = _dy / np.linalg.norm(_dy, axis=1, keepdims=True)
    return _xn, _yn
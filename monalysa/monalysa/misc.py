"""
misc.py is a module with useful functions for various purposes.
"""

from typing import Union, Any
from pandas import Timestamp, Timedelta
import pandas

def is_integer_num(n: Union[int, float]) -> bool:
    """Checks if the given number is an integer.

    Args:
        n (Union[int, float]): The number that is to be checked if it is an
        integer.

    Returns:
        bool: Bool indicating if the number is an integer. True if n is an
        integer, else its False
    """
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False
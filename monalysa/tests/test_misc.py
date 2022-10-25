"""
A set of tests for the monalysa package.

Author: Sivakumar Balasubramanian
Email: siva82kb@gmail.com
Date: 25 Oct 2022
"""

import sys
sys.path.append("..")

from monalysa import misc

import numpy as np


def test_is_integer_num():
    assert misc.is_integer_num(5)
    assert misc.is_integer_num(5.0)
    assert misc.is_integer_num(5.1) == False
    assert misc.is_integer_num(-12)
    assert misc.is_integer_num(-12.3453) == False
    assert misc.is_integer_num('sdagads') == False
    
    
def test_is_binary_signal():
    # Create randomb bindary data
    nsig = 100
    reps = 100
    nnan = 10
    for i in range(reps):
        _sig = np.random.randint(0, 2, nsig)
        
        # Without nans
        assert misc.is_binary_signal(_sig, allownan=True)
        assert misc.is_binary_signal(_sig, allownan=True)
        
        # With random nans.
        _naninx = np.random.randint(0, nsig, 10)
        _signan = 1.0 * _sig.copy()
        _signan[_naninx] = np.NaN
        assert misc.is_binary_signal(_signan, allownan=False) == False
        assert misc.is_binary_signal(_signan, allownan=True)
        
        # Non-binary values.
        _otherinx = np.random.randint(0, nsig, 10)
        _signan[_otherinx] = np.random.randn(nnan)
        assert misc.is_binary_signal(_signan, allownan=False) == False
        assert misc.is_binary_signal(_signan, allownan=True) == False        
        

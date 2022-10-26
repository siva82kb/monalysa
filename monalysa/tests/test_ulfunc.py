"""
A set of tests for the ulfunc sub-package.

Author: Sivakumar Balasubramanian
Email: siva82kb@gmail.com
Date: 26 Oct 2022
"""

import sys
sys.path.append("..")

import monalysa
from monalysa import ulfunc


def test_monalysa_import():
    assert 'misc' in dir(monalysa)
    assert 'readers' in dir(monalysa)
    assert 'preprocess' in dir(monalysa)
    assert 'quality' in dir(monalysa)
    assert 'ulfunc' in dir(monalysa)


def test_ulfunc_import():
    print(dir(monalysa))
    assert 'uluse' in dir(ulfunc)
    assert 'ulint' in dir(ulfunc)
    assert 'measures' in dir(ulfunc)
    assert 'visualizations' in dir(ulfunc)

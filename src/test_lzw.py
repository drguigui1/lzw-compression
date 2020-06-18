# -*- coding: utf-8 -*-

import pytest

from lzw import to_bin, to_dec

########################
# Test: to_bin         #
########################

def test_to_bin_1():
    ref = '0000010011'
    v = 19
    n = 10
    assert to_bin(v, n) == ref

def test_to_bin_2():
    ref = '1001'
    v = 9
    n = 4
    assert to_bin(v, n) == ref

def test_to_bin_3():
    ref = '01001'
    v = 9
    n = 5
    assert to_bin(v, n) == ref

def test_to_bin_4():
    ref = '0000'
    v = 0
    n = 4
    assert to_bin(v, n) == ref

########################
# Test: to_dec         #
########################

def test_to_dec_1():
    ref = 5
    b = '101'
    assert ref == to_dec(b)

def test_to_dec_2():
    ref = 0
    b = '00000'
    assert ref == to_dec(b)

def test_to_dec_3():
    ref = 63
    b = '000111111'
    assert ref == to_dec(b)

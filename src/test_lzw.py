# -*- coding: utf-8 -*-

import pytest

from lzw import to_bin, to_dec, build_dico, compute_size_bits

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

########################
# Test: build_dico     #
########################

def test_build_dico_1():
    s = "abbbc"
    ref = ['%', 'a', 'b', 'c']
    assert build_dico(s) == ref

def test_build_dico_2():
    s = "bbaabbbaabbaaabbbaaa"
    ref = ['%', 'a', 'b']
    assert build_dico(s) == ref

def test_build_dico_3():
    s = ""
    ref = ['%']
    assert build_dico(s) == ref

###########################
# Test: compute_size_bits #
###########################

def test_compute_size_bits_1():
    s = "rererere"
    dico = ['%', 'e', 'r']
    ref = 16
    assert compute_size_bits(s, dico) == ref

def test_compute_size_bits_2():
    s = "abcdefgh"
    dico = ['%', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ref = 32
    assert compute_size_bits(s, dico) == ref

def test_compute_size_bits_3():
    s = "yyy"
    dico = ['%', 'y']
    ref = 3
    assert compute_size_bits(s, dico) == ref

# -*- coding: utf-8 -*-

import pytest

from lzw import to_bin, to_dec, build_dico, compute_size_bits, get_first_nbits

from lzw import compress, decompress

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

###########################
# Test: get_first_nbits   #
###########################

def test_get_first_nbits_1():
    s = "01001100"
    n = 3
    res1, res2 = get_first_nbits(s, n)
    assert res1 == "010"
    assert res2 == "01100"

def test_get_first_nbits_2():
    s = "0000"
    n = 4
    res1, res2 = get_first_nbits(s, n)
    assert res1 == "0000"
    assert res2 == ""

def test_get_first_nbits_3():
    s = "101010101111"
    n = 7
    res1, res2 = get_first_nbits(s, n)
    assert res1 == "1010101"
    assert res2 == "01111"

#############################
# Test: compress/decompress #
#############################

def test_compress_decompress_1():
    s = "ab*cde*fgh*"
    cmp_s, _, dico = compress(s)
    res = decompress(cmp_s, dico)
    assert res == s

def test_compress_decompress_2():
    s = "rererere"
    cmp_s, _, dico = compress(s)
    res = decompress(cmp_s, dico)
    assert res == s

def test_compress_decompress_3():
    s = "coucou"
    cmp_s, _, dico = compress(s)
    res = decompress(cmp_s, dico)
    assert res == s

def test_compress_decompress_4():
    s = "pourquoi pas"
    cmp_s, _, dico = compress(s)
    res = decompress(cmp_s, dico)
    assert res == s

def test_compress_decompress_5():
    s = "abcd*dccacbdda*aaddcba*"
    cmp_s, _, dico = compress(s)
    res = decompress(cmp_s, dico)
    assert res == s

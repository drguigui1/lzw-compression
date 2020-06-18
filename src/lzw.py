# -*- coding: utf-8 -*-

from argparse import ArgumentParser

def build_dico():
    # build the default dictionary
    pass

def to_bin(value, n):
    '''
    Convert the value into binary string representation

    :param value: value to convert
    :param n: number of bit(s) for convertion

    :type value: int
    :type n: int

    :return: string binary representation
    :rtype: string
    '''
    tmp = bin(value).split('b')[1]
    return '0' * (n - len(tmp)) + tmp

def _build_arg_list():
    '''
    Build the list of arguments
    '''
    arg_parser = ArgumentParser(description="LZW compression")
    arg_parser.add_argument('-c', action="store_true", help="Launch the compression")
    arg_parser.add_argument('-u', action="store_true", help="Launch the decompression")
    arg_parser.add_argument('-p', help="Specify the path of the text file")
    return arg_parser.parse_args()

if __name__ == "__main__":
    arg_list = _build_arg_list()
    # TODO

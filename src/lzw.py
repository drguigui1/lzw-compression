# -*- coding: utf-8 -*-

from argparse import ArgumentParser

# build the default dictionary
def build_dico(s):
    '''
    Build the dictionnary according to the symbols in s
    ex: for s="abbbc" -> ['%', 'a', 'b', 'c'] ('%' default special char)

    :param s: input string
    :type s: str

    :return: the list with the default elements
    :rtype: list
    '''
    dic = ['%']
    for c in s:
        if not c in dic:
            dic.append(c)
    return dic

# for compression part
def to_bin(value, n):
    '''
    Convert the value into binary string representation

    :param value: value to convert
    :param n: number of bit(s) for convertion

    :type value: int
    :type n: int

    :return: string binary representation
    :rtype: str
    '''
    tmp = bin(value).split('b')[1]
    return '0' * (n - len(tmp)) + tmp

# for decompression
def to_dec(value):
    '''
    Convert binary string into int representation

    :param value: value to convert

    :type value: string

    :return: Converted value into int
    :rtype: int
    '''
    return int(value, 2)

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

# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import pandas as pd

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
    dic.sort()
    return dic

# for compression part
def to_bin(value, n):
    '''
    Convert the value into binary string representation

    :param value: Value to convert
    :param n: Number of bit(s) for convertion

    :type value: int
    :type n: int

    :return: String binary representation
    :rtype: str
    '''
    tmp = bin(value).split('b')[1]
    return '0' * (n - len(tmp)) + tmp

def compress(s):
    '''
    Compress the input string using the lzw algorithm

    :param s: String to be compressed
    :type s: str

    :return: The compressed string, the lzw table, and the dictionnary
    :rtype: tuple
    '''
    # init the dictionnary
    dic = build_dico(s)
    lzw_table = [['Buffer', 'Input', 'New sequence', 'Address', 'Output']]
    ## TODO

def decompress(s, dico):
    '''
    '''
    pass

def compute_rate():
    '''
    '''
    pass

# write the lzw_table into a csv
def write_csv(table, path):
    '''
    Write the table into a csv file

    :param table: table to write in the file
    :param path: path of the file to write

    :type table: list
    :type path: str
    '''
    cols_name = table[0]
    table = table[1:]
    df = pd.DataFrame(table, columns=cols_name)
    df.to_csv(path, index=False, columns=cols_name)

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
    arg_parser.add_argument('-c', '--compress', action="store_true", help="Launch the compression")
    arg_parser.add_argument('-u', '--uncompress', action="store_true", help="Launch the decompression")
    arg_parser.add_argument('-p', '--path', help="Specify the path of the text file")
    return arg_parser.parse_args()

if __name__ == "__main__":
    arg_list = _build_arg_list()
    path = arg_list.path
    if arg_list.compress:
        # call compression
        # save lzw table into csv
        # save dico into csv
        # save compressed data
        pass
    if arg_list.uncompress:
        # call decompression
        # save decompressed data
        pass


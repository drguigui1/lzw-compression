# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import math
import pandas as pd

########################
#         Utils        #
########################

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

def to_dec(value):
    '''
    Convert binary string into int representation

    :param value: value to convert

    :type value: string

    :return: Converted value into int
    :rtype: int
    '''
    return int(value, 2)

def get_file_content(path):
    '''
    Get the filename according to the string path

    :param path: string path
    :type path: str

    :return: string of the content of the file
    :rtype: str
    '''
    with open(path, 'r+') as f:
        content = f.read()
    # return the content without the eof char
    return content[:-1]

# write a table into a csv
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
    df.to_csv(path, index=False)

def compute_size_bits(s, dico):
    '''
    Compute the number of bits necessary to encode s having the dictionnary dico

    :param s: string not compressed
    :param dico: default dictionnary of s

    :return: return the number if bits necessary to encode s without compression
    '''
    n_bits = math.ceil(math.log(len(dico), 2))
    return len(s) * n_bits

########################
#      Compression     #
########################

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
    default_dico = dic[:]
    n_bits = math.ceil(math.log(len(dic), 2))
    lzw_table = [['Buffer', 'Input', 'New sequence', 'Address', 'Output']]
    compressed_data = ''
    lzw_table.append(['', s[0], '', '', ''])
    buff = s[0]
    addr = ''
    new_seq = ''
    output = ''

    for i in range(1, len(s) + 1):
        idx = dic.index(buff)

        if i == len(s):
            output = '@[' + buff + ']=' + str(idx)
            lzw_table.append([buff, '', '', '', output])
            compressed_data += to_bin(idx, n_bits)
            break

        inpt = s[i]

        new_seq = buff + inpt

        # not in dictionnary
        if not new_seq in dic:
            dic.append(new_seq)
            addr = str(len(dic) - 1)
            output = '@[' + buff + ']=' + str(idx)
            compressed_data += to_bin(idx, n_bits)
            lzw_table.append([buff, inpt, new_seq, addr, output])
            buff = inpt
        # in the dictionnary
        else:
            # condition to augment number of bits for encoding
            output = ''
            idx_new_seq = dic.index(new_seq)
            if idx_new_seq >= 2**n_bits:
                idx_spe = dic.index('%')
                compressed_data += to_bin(idx_spe, n_bits)
                if idx_new_seq == 2 ** n_bits:
                    n_bits += 1
                else:
                    n_bits = int(math.log(math.pow(2, math.ceil(math.log(dic.index(new_seq))/math.log(2))), 2))
                output = '@[%]=' + str(idx_spe)
            lzw_table.append([buff, inpt, '', '', output])
            buff = new_seq

    return compressed_data, lzw_table, default_dico

def save_compressed_data(cmp_content, path, size_content):
    '''
    Save the compressed data into a .lzw file
    Write also size before and after compression and the compression rate

    :param cmp_content: string compressed -> ex: '00011101'
    :param path: path to save data
    :param size_content: size of the data not compressed (number of bits)

    :type cmp_content: str
    :type path: str
    :type size_content: int
    '''
    # size of the compressed data
    size_cmp_content = len(cmp_content)

    # compute the rate
    rate = size_cmp_content / size_content

    # str to save in the lzw file
    str_to_save = ""
    str_to_save += cmp_content + '\n'
    str_to_save += "Size before LZW compression: " + str(size_content) + ' bits \n'
    str_to_save += "Size after LZW compression: " + str(size_cmp_content) + ' bits \n'
    str_to_save += "Compression ratio: " + str(rate)

    # save the data into the file
    with open(path, 'a+') as f:
        f.write(str_to_save)

########################
#     Decompression    #
########################

def get_first_nbits(cmp_data, n_bits):
    '''
    Get the first n bits of cmp_data
    ex: if n_bits = 3 and cmp_data = "010011" -> "010"
    '''
    addr = cmp_data[:n_bits]
    return addr, cmp_data[n_bits:]

def decompress(s, dico):
    '''
    '''
    pass

def save_decompressed_data():
    '''
    '''
    pass

########################
#         Main         #
########################

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
    filename = path.split('/')[-1].split('.')[0]
    if arg_list.compress:
        # get file content
        content = get_file_content(path)

        # call compression
        cmp_content, lzw_table, default_dico = compress(content)

        # save lzw table into csv
        write_csv(lzw_table, './' + filename + '_LZWtable.csv')

        # save dico into csv
        write_csv([default_dico], './' + filename + '_dico.csv')

        # compute the bits size of content
        size_content = compute_size_bits(content, default_dico)

        # save compressed data
        save_compressed_data(cmp_content, './' + filename + '.lzw', size_content)

    if arg_list.uncompress:
        # call decompression
        # save decompressed data
        # TODO
        pass


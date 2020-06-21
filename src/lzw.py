# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import pandas as pd
import numpy as np

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
    n_bits = int(np.ceil(np.log2(len(dico))))
    return len(s) * n_bits

def is_enough_bits(n_bits, addr):
    '''
    Determine according to an address if n_bits is enough to encode addr

    :param n_bits: current number of bits the encode the data
    :param addr: addr to encode

    :type n_bits: int
    :type addr: addr

    :return: wether n_bits is enough to encode addr
    :rtype: bool
    '''
    return addr < 2**n_bits

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
    idx_spe = dic.index('%')
    n_bits = int(np.ceil(np.log2(len(dic))))
    lzw_table = [['Buffer', 'Input', 'New sequence', 'Address', 'Output']]
    lzw_table.append(['', s[0], '', '', ''])
    buff = s[0]
    addr, new_seq, output, compressed_data = '', '', '', ''

    for i in range(1, len(s)):
        idx = dic.index(buff)

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
            idx_new_seq = dic.index(new_seq)
            if (is_enough_bits(n_bits, idx_new_seq)):
                lzw_table.append([buff, inpt, '', '', ''])
            else:
                while (not is_enough_bits(n_bits, idx_new_seq)):
                    lzw_table.append([buff, inpt, '', '', '@[%]=' + str(idx_spe)])
                    compressed_data += to_bin(idx_spe, n_bits)
                    n_bits += 1

            buff = new_seq

    # last element case
    idx = dic.index(buff)
    lzw_table.append([buff, '', '', '', '@[' + buff + ']=' + str(idx)])
    compressed_data += to_bin(idx, n_bits)

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
    str_to_save += "Size before LZW compression: " + str(size_content) + ' bits\n'
    str_to_save += "Size after LZW compression: " + str(size_cmp_content) + ' bits\n'
    str_to_save += "Compression ratio: " + str(rate)

    # save the data into the file
    with open(path, 'a+') as f:
        f.write(str_to_save)

########################
#     Decompression    #
########################

def get_dico_path(file_path):
    '''
    Build the path of dico file (the dico file is in the same dir as file path)

    :param file_path: path of the file
    :type file_path: str
    '''
    pos = file_path.rfind('/')
    filename = file_path.split('/')[-1].split('.')[0]
    return file_path[:pos+1] + filename + '_dico.csv'

def get_default_dico(path):
    '''
    Get the default dico from the csv file

    :param path: path of the csv file
    :type path: str
    '''
    dico = pd.read_csv(path)
    return dico

def get_first_nbits(cmp_data, n_bits):
    '''
    Get the first n bits of cmp_data
    ex: if n_bits = 3 and cmp_data = "010011" -> "010"

    :param cmp_data: compressed data in binary string format -> "001011101"
    :param n_bits: n bits to get from cmp_data

    :type cmp_data: str
    :type n_bits: int

    :return: tuple with the firsts n bits of the compressed data and the rest
    :rtype: tuple
    '''
    addr = cmp_data[:n_bits]
    return addr, cmp_data[n_bits:]

def decompress(cmp_data, dico):
    '''
    Decompress the compressed input data
    '''
    # know on which number bits to read cmp_data
    n_bits = int(np.ceil(np.log2(len(dico))))
    addr, cmp_data = get_first_nbits(cmp_data, n_bits)

    # convert addr to dec
    addr_dec = to_dec(addr)

    # set the default buffer
    buff = dico[addr_dec]

    # last char added into the dictionnary
    last_chr_dico = ''
    output = ''

    while (cmp_data != ""):
        addr, cmp_data = get_first_nbits(cmp_data, n_bits)
        addr_dec = to_dec(addr)

        # already in the dico
        if addr_dec < len(dico):
            inpt_seq = dico[addr_dec]
        # not in the dico (particular case)
        else:
            inpt_seq = buff + last_chr_dico

        # case we receive '%'
        if inpt_seq == '%':
            n_bits += 1
            continue

        new_seq = buff + inpt_seq[0]
        dico.append(new_seq)

        output += buff
        last_chr_dico = new_seq[-1]
        buff = dico[addr_dec]

    # add last element
    output += buff

    return output

def save_decompressed_data(data, path):
    '''
    Save decompressed data into a file

    :param data: data to save into the file
    :param path: path of the file

    :type data: str
    :type path: str
    '''
    f = open(path, 'w+')
    f.write(data)
    f.close()

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
    pos = path.rfind('/')
    filename = path.split('/')[-1].split('.')[0]

    # get file content
    # in case of compression the content is not compressed
    # in case of decompression the content is compressed in binary (string storage)
    content = get_file_content(path)

    if arg_list.compress:
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
        # build the dico path
        path_dico = get_dico_path(path)

        # get the default dictionnary
        default_dico = list(get_default_dico(path_dico))

        # call decompression
        data = decompress(content, default_dico)

        # save decompressed data
        save_decompressed_data(data, filename + '.txt')
        pass


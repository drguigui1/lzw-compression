# -*- coding: utf-8 -*-

from argparse import ArgumentParser

def _build_arg_list():
    '''
    Build the list of arguments
    '''
    arg_parser = ArgumentParser(description="LZW compression")
    arg_parser.add_argument('-c', action="store_true", help="Launch the compression")
    arg_parser.add_argument('-p', help="Specify the path of the text file")
    return arg_parser.parse_args()

if __name__ == "__main__":
    arg_list = _build_arg_list()
    # TODO

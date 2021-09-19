
import os
import sys
import argparse

from logger import logger
from constants import ILLEGAL_FILENAME_CHARS

def Banner():
    print(u'''
       _   _            _        _
 _ __ | | | | ___ _ __ | |_ __ _(_)
| '_ \| |_| |/ _ \ '_ \| __/ _` | |
| | | |  _  |  __/ | | | || (_| | |
|_| |_|_| |_|\___|_| |_|\__\__,_|_|

''')

def ParseArgs(args):
    
    parser = argparse.ArgumentParser(description='nHentai downloader')
    group = parser.add_mutually_exclusive_group()


    group.add_argument('-d', '--download', dest='download', action='store_true',
        help="download the doujinshi")

    group.add_argument('-I', '--info', dest='show_info', action='store_true',
        help="shows the info about the given doujin")

    parser.add_argument('-i', '--id', type=str, dest='ids', metavar='',
        help="specify the doujinshi ids, ex \"--id 94848,22303,29392\"")

    parser.add_argument('-f', '--format', type=str, dest='name_format', metavar='',
        help='specify the doujinshi folder name format', default='%i')

    parser.add_argument('-o', '--output', type=str, dest='output', metavar='', default='downloads\\',
        help="specify the output directory")

    parser.add_argument('-t', '--threads', type=int, dest='threads', metavar='', default=5,
        help="specify the number of threads")

    parser.add_argument('-T', '--timeout', type=int, dest='timeout', metavar='', default=30,
        help='specify the request timeout')

    parser.add_argument('-D', '--delay', type=int, dest='delay', metavar='', default=0,
        help='set delay between downloads')

    parser.add_argument('-hf', '--html-format', dest='html_format', type=str, metavar='', default='default',
        help='the html template to use')

    parser.add_argument('-nh', '--no-html', dest='generate_html',  action='store_false',
        help='should an html viewer be created after downloading')

    parser.add_argument('-nm', '--no-meta', dest='generate_meta_file',  action='store_false',
        help='should the doujin meta be saved in a json file')

    # Add login / cookie usage
    # Add search functionality


    args = parser.parse_args(args)

    if not args.download and not args.show_info:
        logger.critical("No operation specified, use -h for help")
        quit(1)

    if args.ids == None:
        logger.critical("No doujinshi ids specified")
        quit(1)

    else:
        _ = [i.strip() for i in args.ids.split(',')]
        args.ids = set(int(i) for i in _ if i.isdigit())

    if args.output:
        has_c = args.output.find(":")
        if any([args.output.find(i) != -1 for i in ILLEGAL_FILENAME_CHARS] or (has_c != 1 and has_c != -1)):
            logger.critical("Output directory contains illegal characters")
            quit(1)

    if args.name_format:
        has_c = args.output.find(":")
        if any([args.name_format.find(i) != -1 for i in ILLEGAL_FILENAME_CHARS] or (has_c != 1 and has_c != -1)):
            logger.critical("Name format contains illegal characters")
            quit(1)

    if args.html_format not in ("default", "minimal"):
        logger.critical("Invalid html format")
        quit(1)

    if args.threads < 0:
        args.threads = 1

    if args.delay < 0:
        args.delay = 0

    if args.timeout < 0:
        args.timeout = 0

    return args

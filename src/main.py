


import os
import sys
import json
import time

from logger import logger
from constants import USER_AGENT ,BASE_URL,PAGE_URL,SEARCH_URL,LOGIN_URL ,IMAGE_URL
from doujinshi import DoujinshiInfo, Doujinshi
from downloader import Downloader, Get_Douijinshi
from cmdline import ParseArgs, Banner
from helpers import Generate_Html


def main():
    downl = Downloader()
    
    args = ParseArgs(sys.argv[1:])

    downl.delay = args.delay
    downl.timeout = args.timeout
    downl.size = args.threads
    downl.path = args.output

    doujinshi = []
    for id in args.ids:
        d = Get_Douijinshi(id)
        d.name_format = args.name_format
        d.downloader = downl
        d.Update()
        doujinshi.append(d)

    if args.download:

        for d in doujinshi:

            if args.delay != 0:
                time.sleep(args.delay) 

            d.Download()
            if args.generate_html:
                Generate_Html(args.output, d, args.html_format, args.generate_meta_file)


    else:
        for d in doujinshi:

            print(d) 


    logger.info('All done.')

if __name__ == "__main__":
    Banner()
    main()

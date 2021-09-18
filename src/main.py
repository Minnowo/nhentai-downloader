


import os
import sys
import json
import time

from logger import logger
from constants import USER_AGENT ,BASE_URL,PAGE_URL,SEARCH_URL,LOGIN_URL ,IMAGE_URL, Save_URL_Conf, Load_URL_Conf
from doujinshi import DoujinshiInfo, Doujinshi
from downloader import Downloader, Get_Douijinshi
from cmdline import ParseArgs, Banner



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

    else:
        for d in doujinshi:

            print(d) 


    logger.log(12, 'All done.')

if __name__ == "__main__":
    Banner()
    Load_URL_Conf()
    main()
    Save_URL_Conf()



import os
import sys
import json
import time

try:
    from logger import logger
    from constants import USER_AGENT ,BASE_URL,PAGE_URL,SEARCH_URL,LOGIN_URL ,IMAGE_URL
    from doujinshi import DoujinshiInfo, Doujinshi
    from downloader import Downloader, Get_Douijinshi
    from cmdline import ParseArgs, Banner
    from helpers import Generate_Html_Viewer_, Format_Doujin_String_
except ImportError:
    from src.logger import logger
    from src.constants import USER_AGENT ,BASE_URL,PAGE_URL,SEARCH_URL,LOGIN_URL ,IMAGE_URL
    from src.doujinshi import DoujinshiInfo, Doujinshi
    from src.downloader import Downloader, Get_Douijinshi
    from src.cmdline import ParseArgs, Banner
    from src.helpers import Generate_Html_Viewer_, Format_Doujin_String_

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
        d.Update_Name_Format(args.name_format)
        doujinshi.append(d)

    if args.sauce_file:
        for d in doujinshi:

            if args.delay != 0:
                time.sleep(args.delay) 

            Generate_Html_Viewer_(args.output, Format_Doujin_String_(d, args.sauce_file_output), d, args.html_format, args.generate_meta_file, True) 

    elif args.download:

        for d in doujinshi:

            if args.delay != 0:
                time.sleep(args.delay) 

            d.downloader = downl
            d.Download()
            
            if args.generate_html:
                Generate_Html_Viewer_(os.path.join(args.output, d.formated_name), "index.html", d, args.html_format, args.generate_meta_file, False)


    else:
        for d in doujinshi:

            print(d) 


    logger.info('All done.')

if __name__ == "__main__":
    Banner()
    main()

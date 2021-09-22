
import os
import sys
import time

try:
    from logger import logger
    from constants import USER_AGENT ,BASE_URL,PAGE_URL,SEARCH_URL,LOGIN_URL ,IMAGE_URL, CONFIG
    from doujinshi import DoujinshiInfo, Doujinshi
    from downloader import Downloader, Get_Douijinshi
    from cmdline import ParseArgs, Banner
    from helpers import Generate_Html_Viewer_, Format_Doujin_String_, serialize_doujinshi
except ImportError:
    from nhentai.logger import logger
    from nhentai.constants import USER_AGENT ,BASE_URL,PAGE_URL,SEARCH_URL,LOGIN_URL ,IMAGE_URL, CONFIG
    from nhentai.doujinshi import DoujinshiInfo, Doujinshi
    from nhentai.downloader import Downloader, Get_Douijinshi
    from nhentai.cmdline import ParseArgs, Banner
    from nhentai.helpers import Generate_Html_Viewer_, Format_Doujin_String_, serialize_doujinshi

def main():
    Banner()
    
    downl = Downloader()
    
    args = ParseArgs(sys.argv[1:])

    if CONFIG['proxy']['http']:
        logger.info('Using proxy: {0}'.format(CONFIG['proxy']['http']))

    downl.delay = args.delay
    downl.timeout = args.timeout
    downl.size = args.threads
    downl.path = args.output

    doujinshi = []
    for id in args.ids:
        d = Get_Douijinshi(id)
        d.Update_Name_Format(args.name_format)
        doujinshi.append(d)

    if args.meta_file:
        for d in doujinshi:

            if args.delay != 0:
                time.sleep(args.delay) 
            
            serialize_doujinshi(d, args.output, d.formated_name + ".metadata.json")

    elif args.sauce_file:
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

            elif args.generate_meta_file:
                serialize_doujinshi(d, args.output)

    else:
        for d in doujinshi:

            logger.info(str(d) + "\n") 


    logger.info('All done.')

if __name__ == "__main__":
    main()

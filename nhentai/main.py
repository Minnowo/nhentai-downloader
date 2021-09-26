
import os
import sys
import time
import signal
import multiprocessing

try:
    from logger import logger
    from constants import USER_AGENT ,BASE_URL,PAGE_URL,SEARCH_URL,LOGIN_URL ,IMAGE_URL, CONFIG
    from doujinshi import DoujinshiInfo, Doujinshi
    from downloader import Downloader
    from cmdline import parse_args, banner
    from helpers import generate_html_viewer_, format_doujin_string_, serialize_doujinshi, signal_handler, generate_main_html
except ImportError:
    from nhentai.logger import logger
    from nhentai.constants import USER_AGENT ,BASE_URL,PAGE_URL,SEARCH_URL,LOGIN_URL ,IMAGE_URL, CONFIG
    from nhentai.doujinshi import DoujinshiInfo, Doujinshi
    from nhentai.downloader import Downloader
    from nhentai.cmdline import parse_args, banner
    from nhentai.helpers import generate_html_viewer_, format_doujin_string_, serialize_doujinshi, signal_handler, generate_main_html

def main():
    banner()

    downl = Downloader()
    
    args = parse_args(sys.argv[1:])

    if args.gen_main:
        generate_main_html(args.output)
        return

    if CONFIG['proxy']['http']:
        logger.info('Using proxy: {0}'.format(CONFIG['proxy']['http']))

    downl.delay = args.delay
    downl.timeout = args.timeout
    downl.size = args.threads
    downl.path = args.output

    doujinshi = []
    for id in args.ids:
        logger.info("Fetching page for {}".format(id))
        d = Downloader.get_douijinshi(id)
        d.update_name_format(args.name_format)
        doujinshi.append(d)

    
    if args.download:

        for d in doujinshi:

            if args.delay != 0:
                time.sleep(args.delay) 

            d.downloader = downl
            d.download()
            d.download()
            
            if args.generate_html:
                generate_html_viewer_(os.path.join(args.output, d.formated_name), "index.html", d, args.html_format, args.generate_meta_file, False)

            elif args.generate_meta_file:
                serialize_doujinshi(d, args.output)

    elif args.sauce_file:
        for d in doujinshi:

            if args.delay != 0:
                time.sleep(args.delay) 

            generate_html_viewer_(args.output, format_doujin_string_(d, args.sauce_file_output), d, args.html_format, args.generate_meta_file, True) 

    elif args.meta_file:
        for d in doujinshi:

            if args.delay != 0:
                time.sleep(args.delay) 
            
            serialize_doujinshi(d, args.output, d.formated_name + ".metadata.json")

    else:
        for d in doujinshi:

            logger.info(str(d) + "\n") 


    logger.info('All done.')


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()

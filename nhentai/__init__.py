
import os
import sys
import time
import signal

from multiprocessing import freeze_support
from . import logger, cmdline, constants, downloader, helpers, meta


def banner():
    logger.logger.info(u'''nHentai ver %s:
       _   _            _        _
 _ __ | | | | ___ _ __ | |_ __ _(_)
| '_ \| |_| |/ _ \ '_ \| __/ _` | |
| | | |  _  |  __/ | | | || (_| | |
|_| |_|_| |_|\___|_| |_|\__\__,_|_|

''' % meta.__version__)


def main():
    signal.signal(signal.SIGINT, helpers.signal_handler)
    
    freeze_support()


    banner()

    downl = downloader.Downloader()
    
    args = cmdline.parse_args(sys.argv[1:])

    if args.gen_main:
        helpers.generate_main_html(args.output)
        logger.logger.info("All done.")
        return 0

    if constants.CONFIG['proxy']['http']:
        logger.logger.info('Using proxy: {0}'.format(constants.CONFIG['proxy']['http']))

    downl.delay = args.delay
    downl.timeout = args.timeout
    downl.size = args.threads
    downl.path = args.output

    doujinshi = []
    for id in args.ids:
        logger.logger.info("Fetching page for {}".format(id))
        d = downloader.Downloader.get_douijinshi(id)
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
                helpers.generate_html_viewer_(os.path.join(args.output, d.formated_name), "index.html", d, args.html_format, args.generate_meta_file, False)

            elif args.generate_meta_file:
                helpers.serialize_doujinshi(d, args.output)

    elif args.sauce_file:
        for d in doujinshi:

            if args.delay != 0:
                time.sleep(args.delay) 

            helpers.generate_html_viewer_(args.output, helpers.format_doujin_string_(d, args.sauce_file_output), d, args.html_format, args.generate_meta_file, True) 

    elif args.meta_file:
        for d in doujinshi:

            if args.delay != 0:
                time.sleep(args.delay) 
            
            helpers.serialize_doujinshi(d, args.output, d.formated_name + ".metadata.json")

    else:
        for d in doujinshi:

            logger.logger.info(str(d) + "\n") 


    logger.logger.info('All done.') 
    return 0

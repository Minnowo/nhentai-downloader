# coding: utf-

import multiprocessing
import signal

import sys
import os
import requests
import time
import re

from urllib.parse import urlparse
from helpers import Create_Directory, Request_Helper
from constants import PAGE_URL, IMAGE_URL
from bs4 import BeautifulSoup
from doujinshi import Doujinshi, DoujinshiInfo
from logger import logger

requests.packages.urllib3.disable_warnings()

semaphore = multiprocessing.Semaphore(1)

def Get_Douijinshi(id : int) -> Doujinshi:
    """Gets a Doujinshi object from an nhentai page source"""

    info = dict()

    doujin = Doujinshi()
    doujin.id = id

    page = Get_Doujinshi_Page(id)

    if not page:
        return doujin

    html = BeautifulSoup(page, 'html.parser')

    info_div = html.find('div', attrs={'id': 'info'})

    doujin.name = info_div.find('h1').text
    doujin.pretty_name = info_div.find('h1').find('span', attrs={'class': 'pretty'}).text
    info["Subtitle"] = info_div.find('h2')

    doujinshi_cover = html.find('div', attrs={'id': 'cover'})
    img_id = re.search('/galleries/([0-9]+)/cover.(jpg|png|gif)$',doujinshi_cover.a.img.attrs['data-src']).group(1)

    index = 0
    for i in html.find_all('div', attrs={'class': 'thumb-container'}):
        index += 1
        thumb_url = i.img.attrs['data-src']
        image_url = "%s/%s/%d.%s" % (IMAGE_URL, img_id, index, thumb_url.split(".")[-1])
        doujin.pages.append(image_url)

    doujin.page_count = len(doujin.pages)
    

    needed_fields = [
        'Uploaded', 'Characters', 'Artists', 'Languages', 'Pages'
        'Tags', 'Parodies', 'Groups', 'Categories'
        ]
    
    for field in info_div.find_all('div', attrs={'class': 'field-name'}):

        field_name = field.contents[0].strip().strip(':')

        if field_name in needed_fields:
            data = [s.find('span', attrs={'class': 'name'}).contents[0].strip() for s in field.find_all('a', attrs={'class': 'tag'})]
            info[field_name.lower()] = ', '.join(data)

    time_field = info_div.find('time')
    if time_field.has_attr('datetime'):
        info['uploaded'] = time_field['datetime']

    doujin.info = DoujinshiInfo(**info)
    doujin.Update()

    return doujin


def Get_Doujinshi_Page(id_ : str) -> list:
    """Downloads the source of the given nhentai page."""
    url = '{0}/{1}/'.format(PAGE_URL, id_)

    try:
        response = Request_Helper('get', url)
        
        if response.status_code == 200:
            return response.content

        elif response.status_code == 404:
            logger.error("Doujinshi with id {0} cannot be found".format(id_))
            return None

        else:
            logger.warning('Slow down and retry ({}) ...'.format(id_))
            time.sleep(1)
            return Get_Doujinshi_Page(str(id_))
    except:
        return None


class ImageNotExistsException(Exception):
    pass


class Downloader():

    def __init__(self, path='', size=5, timeout=30, delay=0):

        if not path:self.path = os.path.join(os.getcwd(), "downloads")
        else: self.path = str(path)

        self.size = size
        self.timeout = timeout
        self.delay = delay

    def __Download(self, url, folder='', filename='', retried=0, proxy=None):
        if self.delay:
            time.sleep(self.delay)

        filename = filename if filename else os.path.basename(urlparse(url).path)
        base_filename, extension = os.path.splitext(filename)
        output_filename = os.path.join(folder, base_filename.zfill(3) + extension)

        logger.info('Starting to download {0} ...'.format(url))

        if os.path.exists(output_filename):
            logger.warning('File: {0} exists, ignoring'.format(output_filename))
            return 1, url

        try:

            response = None

            with open(output_filename, "wb") as f:
                
                # Make 10 attempts at downloading item.
                i = 0
                while i < 10:
                    try:
                        response = Request_Helper('get', url, stream=True, timeout=self.timeout, proxies=proxy)
                        if response.status_code != 200:
                            raise ImageNotExistsException

                    except ImageNotExistsException as e:
                        raise e

                    except Exception as e:
                        i += 1
                        if i >= 10:
                            logger.critical(str(e))
                            return 0, None
                        continue

                    break

                length = response.headers.get('content-length')
                if length is None:
                    f.write(response.content)
                else:
                    for chunk in response.iter_content(2048):
                        f.write(chunk)

        except (requests.HTTPError, requests.Timeout) as e:
            if retried < 3:
                return 0, self.__Download(url=url, folder=folder, filename=filename, retried=retried+1, proxy=proxy)
            else:
                return 0, None

        except ImageNotExistsException as e:
            os.remove(os.path.join(folder, base_filename.zfill(3) + extension))
            return -1, url

        except Exception as e:
            logger.critical(str(e))
            return 0, None

        except KeyboardInterrupt:
            return -3, None

        return 1, url

    def __Download_Callback(self, result):
        result, data = result

        if result == 0:
            logger.warning('fatal errors occurred, ignored')

        elif result == -1:
            logger.warning('url {0} return status code 404'.format(data))

        elif result == -2:
            logger.warning('Ctrl-C pressed, exiting sub processes ...')

        elif result == -3:
            pass # workers wont be run, just pass

        else:
            logger.log('{0} downloaded successfully'.format(data))

    def Download(self, queue, folder=''):
        """Start the download queue."""
        folder = str(folder)

        if self.path:
            folder = os.path.join(self.path, folder)

        if not os.path.exists(folder):
            logger.warning('Path \'{0}\' does not exist, creating.'.format(folder))
            Create_Directory(folder)


        queue = [(self, url, folder, None) for url in queue]

        pool = multiprocessing.Pool(self.size, __Init_Worker)
        [pool.apply_async(__Download_Wrapper, args=item) for item in queue]

        pool.close()
        pool.join()


def __Download_Wrapper(obj, url, folder='', proxy=None):
    if sys.platform == 'darwin' or semaphore.get_value():
        return Downloader.__Download(obj, url=url, folder=folder, proxy=proxy)
    else:
        return -3, None


def __Init_Worker():
    signal.signal(signal.SIGINT, __Subprocess_Signal)


def __Subprocess_Signal(signal, frame):
    if semaphore.acquire(timeout=1):
        print('Ctrl-C pressed, exiting sub processes ...')

    raise KeyboardInterrupt





if __name__ == "__main__":

    id = 373233

    d = Get_Douijinshi(id)
    import json
    print("------------------------------")
    print("Name:          %s" % d.name)
    print("Name Pretty:   %s" % d.pretty_name)
    print("Name Formated: %s" % d.formated_name)
    print("Name Format:   %s" % d.name_format)
    print("URL:           %s" % d.url)
    print("------------------------------\n")

    print("Page Count:    %s" % d.page_count)
    print(d.info)
    print("")
    print("")
    print(json.dumps(d.table, indent=1))
    



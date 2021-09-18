
import datetime

from constants import PAGE_URL
from logger import logger
from helpers import Format_Filename

class DoujinshiInfo(dict):
    def __init__(self, **kwargs):
        super(DoujinshiInfo, self).__init__(**kwargs)

    def __getattr__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            return ''


class Doujinshi(object):
    def __init__(self, id=-1, name="", pretty_name="", pages=[], 
    name_format='[%i][%a][%t]', downloader=None, **kwargs):

        self.id = id

        self.name = name
        self.pretty_name = pretty_name
        self.name_format = name_format

        self.pages = pages
        self.page_count = len(self.pages)
        self.downloader = downloader
        self.url = '%s/%d' % (PAGE_URL, self.id)
        self.info = DoujinshiInfo(**kwargs)

        _name_format = name_format.replace('%i', str(self.id))
        _name_format = _name_format.replace('%a', self.info.artists)
        _name_format = _name_format.replace('%t', self.name)
        _name_format = _name_format.replace('%p', self.pretty_name)
        _name_format = _name_format.replace('%s', self.info.subtitle)
        self.formated_name = Format_Filename(_name_format)

        self.table = [
            ["Parodies", self.info.parodies],
            ["Doujinshi", self.name],
            ["Subtitle", self.info.subtitle],
            ["Characters", self.info.characters],
            ["Authors", self.info.artists],
            ["Languages", self.info.languages],
            ["Tags", self.info.tags],
            ["URL", self.url],
            ["Pages", self.pages],
            ["Uploaded", self.info.uploaded]
        ]



    def Update(self):
        """Updates the page count, url, and table."""
        self.page_count = len(self.pages)
        self.url = '%s/%d' % (PAGE_URL, self.id)
        self.table = [
            ["Parodies", self.info.parodies],
            ["Doujinshi", self.name],
            ["Subtitle", self.info.subtitle],
            ["Characters", self.info.characters],
            ["Authors", self.info.artists],
            ["Languages", self.info.languages],
            ["Tags", self.info.tags],
            ["URL", self.url],
            ["Pages", self.pages],
            ["Uploaded", self.info.uploaded]
        ]
        _name_format = self.name_format.replace('%i', str(self.id))
        _name_format = _name_format.replace('%a', self.info.artists)
        _name_format = _name_format.replace('%t', self.name)
        _name_format = _name_format.replace('%p', self.pretty_name)
        _name_format = _name_format.replace('%s', self.info.subtitle)
        self.formated_name = Format_Filename(_name_format)


    
    def Download(self):
        """Begin downloading the doujin."""
        logger.info('Starting to download doujinshi: %s' % self.name)

        if not self.downloader:
            logger.error("No downloader has been loaded, cannot download.")
            return

        if self.page_count < 1:
            logger.error("Doujin object has no defined pages.")
            return

        download_queue = []
        for i in self.pages:
            download_queue.append(i)

        self.downloader.Download(download_queue, self.formated_name)



    def __repr__(self):
        out = """Doujinshi information of %d
----------  ------------------------------------------------------------------------
Parodies    %s
Doujinshi   %s
Subtitle    %s
Characters  %s
Authors     %s
Languages   %s
Tags        %s
URL         %s
Pages       %d
Uploaded    %s
----------  ------------------------------------------------------------------------""" % (self.id, self.info.paraodies, self.name, self.info.subtitle, 
        self.info.characters, self.info.artists, self.info.languages, self.info.tags, self.url, self.page_count, 
        datetime.datetime.strptime(self.info.uploaded,"%Y-%m-%dT%H:%M:%S"))

        return out
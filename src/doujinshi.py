
from constants import PAGE_URL
from logger import logger

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
    name_format='[%i][%a][%t]', **kwargs):

        self.id = id

        self.name = name
        self.pretty_name = pretty_name
        self.name_format = name_format

        self.pages = pages
        self.page_count = len(self.pages)
        self.downloader = None
        self.url = '%s/%d' % (PAGE_URL, self.id)
        self.info = DoujinshiInfo(**kwargs)

        _name_format = name_format.replace('%i', str(self.id))
        _name_format = name_format.replace('%a', self.info.artists)
        _name_format = name_format.replace('%t', self.name)
        _name_format = name_format.replace('%p', self.pretty_name)
        _name_format = name_format.replace('%s', self.info.subtitle)
        self.formated_name = _name_format#format_filename(name_format)

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


    
    def Download(self):
        """Begin downloading the doujin."""
        logger.log('Starting to download doujinshi: %s' % self.name)

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
        return '<Doujinshi: {0}>'.format(self.name)
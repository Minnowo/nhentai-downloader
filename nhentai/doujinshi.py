
import datetime

from . import constants, logger, helpers


class DoujinshiInfo(dict):
    def __init__(self, **kwargs):
        super(DoujinshiInfo, self).__init__(**kwargs)

    def __getattr__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            return ''


class Doujinshi(object):
    def __init__(self, id=-1, name="", pretty_name="",
    name_format='%i', downloader=None, **kwargs):

        self.id = id

        self.name = name
        self.pretty_name = helpers.format_pretty_name(pretty_name)
        self.name_format = name_format

        self.pages = [] # forgot that python defines function defaults at runtime, this NEEDS to be here not in the __init__
        self.page_count = len(self.pages)
        self.downloader = downloader
        self.url = '%s/%d' % (constants.PAGE_URL, self.id)
        self.info = DoujinshiInfo(**kwargs)

        _name_format = name_format.replace('%i', str(self.id))
        _name_format = _name_format.replace('%a', self.info.artists)
        _name_format = _name_format.replace('%t', self.name)
        _name_format = _name_format.replace('%p', self.pretty_name)
        _name_format = _name_format.replace('%s', self.info.subtitle)
        self.formated_name = helpers.format_filename(_name_format)

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


    def update_name_format(self, new_name_format):
        """Updates the name format, and the formated name."""
        self.name_format = new_name_format
        _name_format = new_name_format.replace('%i', str(self.id))
        _name_format = _name_format.replace('%a', self.info.artists)
        _name_format = _name_format.replace('%t', self.name)
        _name_format = _name_format.replace('%p', self.pretty_name)
        _name_format = _name_format.replace('%s', self.info.subtitle)
        self.formated_name = helpers.format_filename(_name_format)


    def update(self):
        """Updates the page count, url, and table."""
        self.page_count = len(self.pages)
        self.url = '%s/%d' % (constants.PAGE_URL, self.id)
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

    
    def download(self):
        """Begin downloading the doujin."""
        logger.logger.info('Starting to download doujinshi: %s' % self.pretty_name)

        if not self.downloader:
            logger.logger.error("No downloader has been loaded, cannot download.")
            return

        if self.page_count < 1:
            logger.logger.error("Doujin object has no defined pages.")
            return

        download_queue = []
        for i in self.pages:
            download_queue.append(i)

        self.downloader.download(download_queue, self.formated_name)



    def __repr__(self):
        date = self.info.uploaded
        try: date = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S")
        except:pass

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
        self.info.characters, self.info.artists, self.info.languages, self.info.tags, self.url, self.page_count, date        )

        return out
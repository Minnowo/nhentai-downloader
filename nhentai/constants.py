import os 
import json
import tempfile

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


USER_AGENT = "nhentai command line client (https://github.com/RicterZ/nhentai) edit by Alice Nyaa ;3c"

ILLEGAL_FILENAME_CHARS = "?*\"<>|"

BASE_URL = os.getenv('NHENTAI', 'https://nhentai.net')

PAGE_URL      = '%s/g' % BASE_URL
SEARCH_URL    = '%s/api/galleries/search' % BASE_URL

TAG_API_URL   = '%s/api/galleries/tagged' % BASE_URL
LOGIN_URL     = '%s/login/' % BASE_URL
CHALLENGE_URL = '%s/challenge' % BASE_URL
FAV_URL       = '%s/favorites/' % BASE_URL

u = urlparse(BASE_URL)
IMAGE_URL = '%s://i.%s/galleries' % (u.scheme, u.hostname)

NHENTAI_HOME = os.path.join(os.getenv('HOME', tempfile.gettempdir()), '.nhentai')
NHENTAI_HISTORY = os.path.join(NHENTAI_HOME, 'history.sqlite3')
NHENTAI_CONFIG_FILE = os.path.join(NHENTAI_HOME, 'config.json')

CONFIG = {
    'proxy': {'http': '', 'https': ''},
    'cookie': '',
    'language': '',
}

LANGUAGEISO ={
    'english' : 'en',
    'chinese' : 'zh',
    'japanese' : 'ja',
    'translated' : 'translated'
}

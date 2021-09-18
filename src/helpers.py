

import os
import requests

from logger import logger
from constants import LOGIN_URL, USER_AGENT, ILLEGAL_FILENAME_CHARS

def Format_Filename(path : str) -> str:
    
    for char in ILLEGAL_FILENAME_CHARS:
        path = path.replace(char, "")

    while path.endswith("."):
        path = path[:-1]

    if len(path) > 100:
        path = path[:100] + u'…'

    return path


def Create_Directory_From_File_Name(path : str) -> str:
    Create_Directory(os.path.dirname(path))


def Create_Directory(path : str) -> bool:
    try:
        os.makedirs(path)
    except Exception as e:
        logger.error(str(e))
    return os.path.isdir(path)


def Request_Helper(method : str, url : str, **kwargs):
    session = requests.Session()
    session.headers.update({
        'Referer': LOGIN_URL,
        'User-Agent': USER_AGENT,
        'Cookie': ''
        })
    
    return getattr(session, method)(url, verify=False, **kwargs)


def signal_handler(signal, frame):
    logger.error('Ctrl-C signal received. Stopping...')
    exit(1)
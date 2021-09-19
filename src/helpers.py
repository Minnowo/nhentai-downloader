

import os
import requests
import json
import sys

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


def Read_File(path):
    loc = os.path.dirname(__file__)

    with open(os.path.join(loc, path), 'r') as file:
        return file.read()

def Write_Text(path, text):

    if sys.version_info < (3, 0):
            with open(path, 'w') as f:
                f.write(text)

    else:
        with open(path, 'wb') as f:
            f.write(text.encode('utf-8'))


def Generate_Html(output_dir='.', doujinshi_obj=None, template='default', generate_meta=True):

    if doujinshi_obj is None:
        logger.warning("Doujinshi object is null cannot create html.")
        return

    doujinshi_dir = os.path.join(output_dir, doujinshi_obj.formated_name)

    if not os.path.isdir(doujinshi_dir):
        logger.warning('Path \'{0}\' does not exist, creating.'.format(doujinshi_dir))

        if not Create_Directory(doujinshi_dir):
            logger.critical("Cannot create output directory.")

    file_list = os.listdir(doujinshi_dir)
    file_list.sort()

    image_html = ''
    for image in file_list:
        if os.path.splitext(image)[1] in ('.jpg', '.png'):
            image_html += '<img src="{0}" class="image-item"/>\n'.format(image)

    html = Read_File('viewer/{}/index.html'.format(template))
    css = Read_File('viewer/{}/styles.css'.format(template))
    js = Read_File('viewer/{}/scripts.js'.format(template))

    if generate_meta:
        serialize_doujinshi(doujinshi_obj, doujinshi_dir)

    name = doujinshi_obj.name if sys.version_info < (3,0) else doujinshi_obj.name.encode('utf-8')
    data = html.format(TITLE=name, IMAGES=image_html, SCRIPTS=js, STYLES=css)

    try:

        html_dir = os.path.join(doujinshi_dir, 'index.html')
        Write_Text(html_dir, data)

        logger.info('HTML Viewer has been written to \'{0}\''.format(html_dir))

    except Exception as e:
        logger.warning('Writing HTML Viewer failed ({})'.format(str(e)))




def serialize_doujinshi(doujinshi, dir):
    metadata = {'title': doujinshi.name,
                'subtitle': doujinshi.info.subtitle
                }

    if doujinshi.info.date:
        metadata['upload_date'] = doujinshi.info.date

    if doujinshi.info.parodies:
        metadata['parody'] = [i.strip() for i in doujinshi.info.parodies.split(',')]

    if doujinshi.info.characters:
        metadata['character'] = [i.strip() for i in doujinshi.info.characters.split(',')]

    if doujinshi.info.tags:
        metadata['tag'] = [i.strip() for i in doujinshi.info.tags.split(',')]

    if doujinshi.info.artists:
        metadata['artist'] = [i.strip() for i in doujinshi.info.artists.split(',')]

    if doujinshi.info.groups:
        metadata['group'] = [i.strip() for i in doujinshi.info.groups.split(',')]

    if doujinshi.info.languages:
        metadata['language'] = [i.strip() for i in doujinshi.info.languages.split(',')]

    if doujinshi.info.uploaded:
        metadata['uploaded'] = doujinshi.info.uploaded

    metadata['category'] = doujinshi.info.categories
    metadata['URL'] = doujinshi.url
    metadata['Pages'] = doujinshi.pages

    try:
        with open(os.path.join(dir, 'metadata.json'), 'w') as f:
            json.dump(metadata, f, separators=(',', ':'), indent=3)

        logger.info('Metadata has been written to \'{0}\\metadata.json\''.format(dir))

    except Exception as e:
        logger.warning('Writing Metadata failed ({})'.format(str(e)))
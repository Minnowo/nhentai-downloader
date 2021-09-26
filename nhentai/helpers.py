

import os
from signal import SIGINT
import requests
import json
import sys

try:
    from logger import logger
    from constants import LOGIN_URL, USER_AGENT, ILLEGAL_FILENAME_CHARS, CONFIG
except ImportError:
    from nhentai.logger import logger
    from nhentai.constants import LOGIN_URL, USER_AGENT, ILLEGAL_FILENAME_CHARS, CONFIG


def format_filename(path : str) -> str:
    """Formats the given path to prevent illegal characters in the filename, removes '.' at the end, 
        and truncates if its longer than 100 chars"""
    for char in ILLEGAL_FILENAME_CHARS:
        path = path.replace(char, "")

    while path.endswith("."):
        path = path[:-1]

    if len(path) > 100:
        path = path[:100] + u'…'

    return path


def create_directory_from_file_name(path : str) -> bool:
    return create_directory(os.path.dirname(path))


def create_directory(path : str) -> bool:
    try:os.makedirs(path)
    except:pass
    return os.path.isdir(path)


def request_helper(method : str, url : str, **kwargs) -> object:
    session = requests.Session()
    session.headers.update({
        'Referer': LOGIN_URL,
        'User-Agent': USER_AGENT,
        'Cookie': CONFIG['cookie']
        })
    
    if not kwargs.get('proxies', None):
        kwargs['proxies'] = CONFIG['proxy']

    return getattr(session, method)(url, verify=False, **kwargs)


def format_doujin_string_(doujin : object, string : str) -> str:
    """Formats the given string with information from the given doujin."""
    _name_format = string.replace('%i', str(doujin.id))
    _name_format = _name_format.replace('%a', doujin.info.artists)
    _name_format = _name_format.replace('%t', doujin.name)
    _name_format = _name_format.replace('%p', doujin.pretty_name)
    _name_format = _name_format.replace('%s', doujin.info.subtitle)

    return _name_format


def signal_handler(signal, frame):
    logger.error('Ctrl-C signal received. Stopping...')
    
    # sys.exit exists the thread, but downloadaer.py ~ line 123 
    # multiprocessing.pool hangs on the pool.join() call, if KeyboardInterrupt
    # kills the processes, which blocks the main thread, making sys.exit do nothing

    # sys.exit(1)

    # this kills the process regardless of if pool.join() is blocking because of the bug
    os.kill(os.getpid(), SIGINT) 

    # can also use
    # os._exit(0)
    


def read_file(path : str) -> str:
    """Reads a file in the same directory as this script"""
    loc = os.path.dirname(__file__)

    with open(os.path.join(loc, path), 'r') as file:
        return file.read()

def write_text(path : str, text : str) -> str:
    """Writes text to the given file"""
    if sys.version_info < (3, 0):
            with open(path, 'w') as f:
                f.write(text)

    else:
        with open(path, 'wb') as f:
            f.write(text.encode('utf-8'))


def generate_html_viewer_(output_dir='.', output_file_name="index.html", doujinshi_obj=None, template='default', generate_meta=True, sauce_file=False):
    """Generates the html viewer for the given doujin"""
    if doujinshi_obj is None:
        logger.warning("Doujinshi object is null cannot create html.")
        return

    if template not in ("minimal", "default"):
        logger.warning("invalid html viewer format, cannot create html.")
        return

    html_dir = os.path.join(output_dir, output_file_name)

    if not create_directory_from_file_name(html_dir):
        logger.critical("Cannot create output directory for html: '{}'".format(os.path.dirname(html_dir)))
        if generate_meta:
            if sauce_file:
                serialize_doujinshi(doujinshi_obj, output_dir, output_file_name + ".metadata.json")
            else:
                serialize_doujinshi(doujinshi_obj, output_dir)
        return


    image_html = ''
    if sauce_file:
        for image in doujinshi_obj.pages:
            image_html += '<img src="{0}" class="image-item"/>\n'.format(image)
    else:
        file_list = os.listdir(output_dir)
        file_list.sort()
        for image in file_list:
            if os.path.splitext(image)[1] in ('.jpg', '.png'):
                image_html += '<img src="{0}" class="image-item"/>\n'.format(image)

    html = read_file('viewer/{}/index.html'.format(template))
    css = read_file('viewer/{}/styles.css'.format(template))
    js = read_file('viewer/{}/scripts.js'.format(template))

    if generate_meta:
        if sauce_file:
            serialize_doujinshi(doujinshi_obj, output_dir, output_file_name + ".metadata.json")
        else:
            serialize_doujinshi(doujinshi_obj, output_dir)

    name = doujinshi_obj.name if sys.version_info < (3,0) else doujinshi_obj.name.encode('utf-8')
    data = html.format(TITLE=name, IMAGES=image_html, SCRIPTS=js, STYLES=css)

    try:

        write_text(html_dir, data)

        logger.info('HTML Viewer has been written to \'{0}\''.format(html_dir))

    except Exception as e:
        logger.warning('Writing HTML Viewer failed ({})'.format(str(e)))




def serialize_doujinshi(doujinshi, dir, file_name = "metadata.json"):
    metadata = {'title': doujinshi.name,
                'title_pretty' : doujinshi.pretty_name,
                'subtitle': doujinshi.info.subtitle
                }

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
    metadata['page count'] = doujinshi.page_count
    metadata['Pages'] = doujinshi.pages

    out_path = os.path.join(dir, file_name)

    if not create_directory_from_file_name(out_path):
        logger.critical("Cannot create output directory for metadata: '{}'".format(os.path.dirname(out_path)))
        return

    try:
        with open(out_path, 'w') as f:
            json.dump(metadata, f, separators=(',', ':'), indent=3)

        logger.info('Metadata has been written to \'{0}\''.format(out_path))

    except Exception as e:
        logger.warning('Writing Metadata failed ({})'.format(str(e)))



# def generate_main_html(output_dir='./'):
#     """
#     Generate a main html to show all the contain doujinshi.
#     With a link to their `index.html`.
#     Default output folder will be the CLI path.
#     """

#     image_html = ''

#     main = Read_File('viewer/main.html')
#     css = Read_File('viewer/main.css')
#     js = Read_File('viewer/main.js')

#     element = '\n\
#             <div class="gallery-favorite">\n\
#                 <div class="gallery">\n\
#                     <a href="./{FOLDER}/index.html" class="cover" style="padding:0 0 141.6% 0"><img\n\
#                             src="./{FOLDER}/{IMAGE}" />\n\
#                         <div class="caption">{TITLE}</div>\n\
#                     </a>\n\
#                 </div>\n\
#             </div>\n'

#     os.chdir(output_dir)
#     doujinshi_dirs = next(os.walk('.'))[1]

#     for folder in doujinshi_dirs:
#         files = os.listdir(folder)
#         files.sort()

#         if 'index.html' in files:
#             logger.info('Add doujinshi \'{}\''.format(folder))
#         else:
#             continue

#         image = files[0]  # 001.jpg or 001.png
#         if folder is not None:
#             title = folder.replace('_', ' ')
#         else:
#             title = 'nHentai HTML Viewer'

#         image_html += element.format(FOLDER=folder, IMAGE=image, TITLE=title)
#     if image_html == '':
#         logger.warning('No index.html found, --gen-main paused.')
#         return
#     try:
#         data = main.format(STYLES=css, SCRIPTS=js, PICTURE=image_html)
#         if sys.version_info < (3, 0):
#             with open('./main.html', 'w') as f:
#                 f.write(data)
#         else:
#             with open('./main.html', 'wb') as f:
#                 f.write(data.encode('utf-8'))
#         shutil.copy(os.path.dirname(__file__) + '/viewer/logo.png', './')
#         set_js_database()
#         logger.log(
#             15, 'Main Viewer has been written to \'{0}main.html\''.format(output_dir))
#     except Exception as e:
#         logger.warning('Writing Main Viewer failed ({})'.format(str(e)))
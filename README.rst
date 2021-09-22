nhentai
=======

.. code-block::

           _   _            _        _
     _ __ | | | | ___ _ __ | |_ __ _(_)
    | '_ \| |_| |/ _ \ '_ \| __/ _` | |
    | | | |  _  |  __/ | | | || (_| | |
    |_| |_|_| |_|\___|_| |_|\__\__,_|_|



nHentai is a CLI tool for downloading doujinshi from <http://nhentai.net>  
this is a modified copy of <https://github.com/RicterZ/nhentai>

===================
Manual Installation
===================
.. code-block::

    git clone https://github.com/Minnowo/nhentai-downloader
    cd nhentai
    python setup.py install




=====
Usage
=====
**IMPORTANT**: To bypass the nhentai frequency limit, you should use `--cookie` option to store your cookie.

*The default download folder will be the path where you run the command + '/downloads/' (CLI path).*


Set your nhentai cookie against captcha:

.. code-block:: bash

    nhentai --cookie "YOUR COOKIE FROM nhentai.net"

**NOTE**: The format of the cookie is `"csrftoken=TOKEN; sessionid=ID"`

| To get csrftoken and sessionid, first login to your nhentai account in web browser, then:
| (Chrome) |ve| |ld| More tools    |ld| Developer tools     |ld| Application |ld| Storage |ld| Cookies |ld| https://nhentai.net
| (Firefox) |hv| |ld| Web Developer |ld| Web Developer Tools                  |ld| Storage |ld| Cookies |ld| https://nhentai.net
| 

.. |hv| unicode:: U+2630 .. https://www.compart.com/en/unicode/U+2630
.. |ve| unicode:: U+22EE .. https://www.compart.com/en/unicode/U+22EE
.. |ld| unicode:: U+2014 .. https://www.compart.com/en/unicode/U+2014

Download specified doujinshi:

.. code-block:: bash

    nhentai --id=123855,123866 -d
    or
    nhentai --id 123855,123866 --download


Format output doujinshi folder name:

.. code-block:: bash

    nhentai --id 261100 --format %i-%p

Supported doujinshi folder formatter:

- %i: Doujinshi id
- %t: Doujinshi name
- %s: Doujinshi subtitle (translated name)
- %a: Doujinshi authors' name
- %p: Doujinshi pretty name



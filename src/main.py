
import os
import sys

from constants import USER_AGENT ,BASE_URL,PAGE_URL,SEARCH_URL,LOGIN_URL ,IMAGE_URL, Save_URL_Conf, Load_URL_Conf
from doujinshi import DoujinshiInfo, Doujinshi
from downloader import Downloader, Get_Douijinshi


def main():

    
    downl = Downloader()
    
    id = 373233

    doujin = Get_Douijinshi(id)
    doujin.downloader = downl
    doujin.formated_name = "test_doujinshi"
    doujin.Update()
    doujin.Download()


if __name__ == "__main__":
    Load_URL_Conf()
    main()
    Save_URL_Conf()
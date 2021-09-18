
import os
import sys
import json

from logger import logger
from constants import USER_AGENT ,BASE_URL,PAGE_URL,SEARCH_URL,LOGIN_URL ,IMAGE_URL, Save_URL_Conf, Load_URL_Conf
from doujinshi import DoujinshiInfo, Doujinshi
from downloader import Downloader, Get_Douijinshi
from cmdline import CMD_Parser, CMD_Command



def main():

    parser = CMD_Parser()
    downl = Downloader()
    
    def Download(id):
        doujin = Get_Douijinshi(id)
        doujin.downloader = downl
        doujin.formated_name = "test_doujinshi"
        doujin.Update()
        doujin.Download()
    

    parser.Add(CMD_Command("--id", "int", Download))

    args= sys.argv[1:]


    print(args)
    parser.Parse_Coms(args)
    # id = 373233

    # doujin = Get_Douijinshi(id)
    # doujin.downloader = downl
    # doujin.formated_name = "test_doujinshi"
    # doujin.Update()
    # doujin.Download()


if __name__ == "__main__":
    Load_URL_Conf()
    main()
    Save_URL_Conf()
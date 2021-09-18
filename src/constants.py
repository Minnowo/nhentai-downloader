import os 
import json
from logger import logger

USER_AGENT = "nhentai command line client (https://github.com/RicterZ/nhentai) edit by Alice Nyaa ;3c"

BASE_URL = "https://nhentai.net"
PAGE_URL = "%s/g" % BASE_URL
SEARCH_URL = "%s/api/galleries/search" % BASE_URL
LOGIN_URL = '%s/login/' % BASE_URL

IMAGE_URL = "https://i.nhentai.net/galleries"

def Load_URL_Conf():
    try:
        if os.path.exists("config.json"):
            with open("config.json", "r") as conf:
                config = json.load(conf)

                if config["nHentai"]:
                    BASE_URL = config["nHentai"]

                if config["page"]:
                    PAGE_URL = config["page"]

                if config["search"]:
                    SEARCH_URL = config["search"]

                if config["login"]:
                    LOGIN_URL = config["login"]

                if config["image"]:
                    IMAGE_URL = config["image"]
            
            logger.log("Url config loaded successfully.")
    except Exception as e:
        logger.error("Unable to load url congif: %s" % e)

def Save_URL_Conf():
    try:
        with open("config.json", "w") as conf:

            config = {
                "nHentai" : BASE_URL,
                "page" : PAGE_URL,
                "search" : SEARCH_URL,
                "login" : LOGIN_URL,
                "image" : IMAGE_URL
            }

            json.dump(config, conf, indent = 3)
        logger.log("Url config loaded successfully.")
    except Exception as e:
        logger.error("Unable to save url config: %s" % e)
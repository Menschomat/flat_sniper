import re
import random
import telegram
import tzlocal
import requests
import asyncio
import storage
from datetime import datetime
from bs4 import BeautifulSoup
import time

from connectors.connector import Connector


def build_flat(article):
    e_id = re.search(r"(?<=lnkToDetails_)\d*",
                     article.find("a", {"id": re.compile("^lnkToDetails_\\d*")}).get("id")).group(0)
    return {
        "exposeId": "immonet_" + e_id,
        "title": re.sub(r"[\n\t\s]*", "",
                        article.find("a", {"id": re.compile("^lnkToDetails_\\d*")}).find(text=True, recursive=False)),
        "price": re.sub(r"[\n\t\s]*", "",
                        article.find("div", {"id": re.compile("^selPrice_\\d*")}).contents[3].find(text=True,
                                                                                                   recursive=False)) + " €",
        "size": re.sub(r"[\n\t\s]*", "",
                       article.find("div", {"id": re.compile("^selArea_\\d*")}).contents[3].find(text=True,
                                                                                                 recursive=False)) + " m²",
        "rooms": re.sub(r"[\n\t\s]*", "",
                        article.find("div", {"id": re.compile("^selRooms_\\d*")}).contents[3].find(text=True,
                                                                                                   recursive=False)),
        "address": re.sub(r"[\n\t]*", "",
                          article.select("div.box-25.ellipsis>span.text-100")[0].find(text=True, recursive=False)),
        "link": "https://www.immonet.de/angebot/" + e_id
    }


class ImmonetConnector(Connector):

    async def fetch_articles(self, url, fetch_min, fetch_max):
        while True:
            print("fetching immonet!")
            page = requests.get(url)
            data = storage.get_storage()
            soup = BeautifulSoup(page.content, 'html.parser')
            articles = soup.find_all("div", {"id": re.compile("^selObject_\\d*")})
            flats = [build_flat(article) for article in articles]
            flats.reverse()
            for flat in flats:
                if flat['exposeId'] not in data:
                    data[flat['exposeId']] = {"storage": flat,
                                              "date_time": datetime.now(tzlocal.get_localzone()).strftime(
                                                  "%Y-%m-%d %H:%M:%S %z")}
                    storage.set_storage(data)
                    time.sleep(random.randint(1, 5))
                    telegram.send_flat(flat)
            await asyncio.sleep(random.randint(450, 750))

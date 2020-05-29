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
    return {
        "exposeId": "immoscout_" + article.get('data-obid'),
        "title": article.find("h5", {"class": "result-list-entry__brand-title"}).find(text=True, recursive=False),
        "price": article.find_all("dl", {"class": "result-list-entry__primary-criterion"})[0].find(
            text=re.compile(r'^.*\s€')),
        "size": article.find_all("dl", {"class": "result-list-entry__primary-criterion"})[1].find(
            text=re.compile(r'^.*\sm²')),
        "rooms": article.find("abbr", text='Zi.').find_parent("dl").find(
            text=re.compile(r'^\d*,?\d*')) if article.find("abbr", text='Zi.') else "Unknown",
        "address": article.find("button", {"class": "result-list-entry__map-link"}).find(text=True,
                                                                                         recursive=False),
        "link": "https://www.immobilienscout24.de/expose/" + article.get('data-obid') + "#/"
    }


class ImmoscoutConnector(Connector):

    async def fetch_articles(self, url, fetch_min, fetch_max):
        while True:
            print("fetching immoscout!")
            page = requests.get(url)
            data = storage.get_storage()
            soup = BeautifulSoup(page.content, 'html.parser')
            articles = soup.find_all("article", {"class": "result-list-entry"})
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

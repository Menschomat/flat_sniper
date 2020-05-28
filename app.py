import re
import os
import random
import asyncio
import json
import uvicorn
import telegram
import config
import tzlocal
import requests
from datetime import datetime
from fastapi import FastAPI
from bs4 import BeautifulSoup

app = FastAPI()
storage_path = config.get_config()['storage'].get()
storage = {}
if not os.path.exists(storage_path):
    with open(storage_path, 'w') as outfile:
        json.dump({}, outfile)
with open(storage_path) as json_file:
    storage = json.load(json_file)


async def fetch_articles(url):
    while True:
        print("FETCHING!")
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        flats = [build_flat(article) for article in soup.find_all("article", {"class": "result-list-entry"})]
        for flat in flats:
            if flat['exposeId'] not in storage:
                storage[flat['exposeId']] = {"data": flat,
                                             "date_time": datetime.now(tzlocal.get_localzone()).strftime(
                                                 "%Y-%m-%d %H:%M:%S %z")}
                telegram.send_flat(flat)
        with open(storage_path, 'w') as storage_file:
            json.dump(storage, storage_file)
        await asyncio.sleep(random.randint(450, 750))


def build_flat(article):
    return {
        "exposeId": article.get('data-obid'),
        "title": article.find("h5", {"class": "result-list-entry__brand-title"}).find(text=True, recursive=False),
        "price": article.find_all("dl", {"class": "result-list-entry__primary-criterion"})[0].find(
            text=re.compile(r'^.*\s€')),
        "size": article.find_all("dl", {"class": "result-list-entry__primary-criterion"})[1].find(
            text=re.compile(r'^.*\sm²')),
        "rooms": article.find("abbr", text='Zi.').find_parent("dl").find(
            text=re.compile(r'^\d*,?\d*')) if article.find("abbr", text='Zi.') else "Unknown",
        "address": article.find("button", {"class": "result-list-entry__map-link"}).find(text=True, recursive=False),
        "link": "https://www.immobilienscout24.de/expose/" + article.get('data-obid') + "#/"
    }


@app.on_event('startup')
def initial_task():
    for url in config.get_config()['immoscout']['urls'].get():
        asyncio.create_task(fetch_articles(url))


@app.get("/")
def root():
    return storage


if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", loop='asyncio', port=config.get_config()['port'].get())
    except asyncio.CancelledError:
        pass

import asyncio
import uvicorn
import config
import storage
from connectors import immoscout, immonet
from fastapi import FastAPI

app = FastAPI()


@app.on_event('startup')
def initial_task():
    fetch_time_min = config.get_config()['fetch_time_min'] if 'fetch_time_min' in config.get_config() else 450
    fetch_time_max = config.get_config()['fetch_time_max'] if 'fetch_time_max' in config.get_config() else 750
    if 'immoscout' in config.get_config():
        for url in config.get_config()['immoscout']['urls'].get():
            con = immoscout.ImmoscoutConnector()
            asyncio.create_task(con.fetch_articles(url, fetch_time_min, fetch_time_max))
    if 'immonet' in config.get_config():
        for url in config.get_config()['immonet']['urls'].get():
            con = immonet.ImmonetConnector()
            asyncio.create_task(con.fetch_articles(url, fetch_time_min, fetch_time_max))


@app.get("/")
def root():
    return storage.get_storage()


if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", loop='asyncio', port=config.get_config()['port'].get())
    except asyncio.CancelledError:
        pass

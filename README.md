# flat_sniper
A little python tool to search for the newest flats, that fit your search-urls.

### Based on:
* Python3.8
* AsyncIO
* FastAPI
* BeautifulSoup
* pyTelegramBotAPI

## Usage
### Configuration:
You'll find a file called `config_default.yaml.example` in the config-folder. Rename it to `config_default.yaml` and 
fill in the credentials for your telegram-bot and your search-urls.
A config should look like this:
````yaml
port: 8080
storage: ./storage.json
immoscout:
  fetch_time_min: 450 // The sheduler fetches data in an random-intervall. It uses a random timespan between min and max, so your requests look more human-like!
  fetch_time_max: 750
  urls:
    - "https://www.immobilienscout24.de/Suche/radius/wohnung-mieten?centerofsearchaddress=Bochum;44892;Ovelackerstra%C3%9Fe;;;Langendreer&numberofrooms=5.0-&geocoordinates=51.47285;7.32158;10.0&sorting=2&enteredFrom=result_l
telegram:
  token: <api-token>
  chat_id: <telegram-chatid>
````
### Docker
TODO
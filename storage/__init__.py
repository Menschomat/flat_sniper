import config
import os
import json

storage_path = config.get_config()['storage'].get()
storage = {}
if not os.path.exists(storage_path):
    with open(storage_path, 'w') as outfile:
        json.dump({}, outfile)
with open(storage_path) as json_file:
    storage = json.load(json_file)


def get_storage():
    return storage


def set_storage(data):
    global storage
    storage = data
    with open(storage_path, 'w') as storage_file:
        json.dump(storage, storage_file)

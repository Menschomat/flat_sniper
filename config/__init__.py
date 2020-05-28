import confuse

config = confuse.LazyConfig('Config', __name__)


def get_config():
    return config

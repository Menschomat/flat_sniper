from abc import ABC, abstractmethod


class Connector(ABC):
    @abstractmethod
    def fetch_articles(self, url, fetch_min, fetch_max):
        pass

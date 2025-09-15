# src/crawlers/base.py

from abc import ABC, abstractmethod
import requests

class Crawler(ABC):
    """
    Abstract base class for all crawlers.
    """

    def __init__(self, api_key):
        self.api_key = api_key

    @abstractmethod
    def fetch_news(self, **kwargs):
        """
        Fetch news from the source.
        Must be implemented by subclasses.
        """
        pass

    def get_json(self, url, params=None, headers=None):
        """
        Helper method to make GET request and return JSON.
        """
        if headers is None:
            headers = {}

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

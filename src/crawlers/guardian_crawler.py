# src/crawlers/guardian_crawler.py

from .base import Crawler

class GuardianCrawler(Crawler):

    BASE_URL = "https://content.guardianapis.com/search"

    def fetch_news(self, keyword=None, from_date=None, to_date=None):
        """
        Fetch news from Guardian API and return standardized format.
        """
        params = {
            "api-key": self.api_key,
            "format": "json"
        }
        if keyword:
            params["q"] = keyword
        if from_date:
            params["from-date"] = from_date
        if to_date:
            params["to-date"] = to_date

        data = self.get_json(self.BASE_URL, params=params)
        results = data.get("response", {}).get("results", [])

        # Normalize results
        news_items = []
        for item in results:
            news_items.append({
                "title": item.get("webTitle"),
                "url": item.get("webUrl"),
                "source": "Guardian",
                "date": item.get("webPublicationDate"),
                "content": None,  # optional, fetch separately if needed
            })
        return news_items

# src/crawlers/guardian_crawler.py

from .base import Crawler
from datetime import datetime, timedelta
from tqdm import tqdm

class GuardianCrawler(Crawler):

    BASE_URL = "https://content.guardianapis.com/search"

    def fetch_news(self, keyword=None, from_date=None, to_date=None):
        """
        Fetch news from Guardian API day by day and return standardized format.
        """
        # Default: last 7 days
        if from_date is None:
            from_date = datetime.today().date() - timedelta(days=7)
        if to_date is None:
            to_date = datetime.today().date()

        # Convert string dates to date objects
        if isinstance(from_date, str):
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        if isinstance(to_date, str):
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

        delta = to_date - from_date
        all_news = []

        for i in tqdm(range(delta.days + 1), desc="Fetching Guardian by day"):
            day = from_date + timedelta(days=i)
            day_str = day.strftime("%Y-%m-%d")

            params = {
                "api-key": self.api_key,
                "format": "json",
                "page-size": 200,
                "from-date": day_str,
                "to-date": day_str,
                "page": 1
            }
            if keyword:
                params["q"] = keyword

            # First request to get total pages
            data = self.get_json(self.BASE_URL, params=params)
            response = data.get("response", {})
            total_pages = response.get("pages", 1)

            for page in range(1, total_pages + 1):
                params["page"] = page
                data = self.get_json(self.BASE_URL, params=params)
                results = data.get("response", {}).get("results", [])

                for item in results:
                    all_news.append({
                        "title": item.get("webTitle"),
                        "url": item.get("webUrl"),
                        "source": "Guardian",
                        "date": item.get("webPublicationDate"),
                        "content": None,
                    })

        return all_news

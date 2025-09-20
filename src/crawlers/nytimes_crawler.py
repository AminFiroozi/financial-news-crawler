# src/crawlers/nytimes_crawler.py

from .base import Crawler
from pynytimes import NYTAPI
from datetime import date, datetime

class NYTimesCrawler(Crawler):

    def __init__(self, api_key):
        super().__init__(api_key)
        self.client = NYTAPI(api_key, parse_dates=True)

    def fetch_news(self, from_date=None, to_date=None):
        """
        Fetch news from NYTimes Archive API within a date range and return standardized format.

        :param from_date: str or date, e.g. "2024-01-01"
        :param to_date: str or date, e.g. "2024-03-15"
        :return: List of normalized articles
        """
        # Default: full current year
        if from_date is None:
            from_date = date.today().replace(month=1, day=1)
        if to_date is None:
            to_date = date.today()

        # Convert str -> date if needed
        if isinstance(from_date, str):
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        if isinstance(to_date, str):
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

        news_items = []

        # Loop through all months in range
        year = from_date.year
        while year <= to_date.year:
            start_month = from_date.month if year == from_date.year else 1
            end_month = to_date.month if year == to_date.year else 12

            for month in range(start_month, end_month + 1):
                print(f"Fetching NYTimes articles for {year}-{month:02d}...")
                archive_data = self.client.archive_metadata(date=date(year, month, 1))

                for article in archive_data:
                    pub_date = article.get("pub_date")
                    if isinstance(pub_date, datetime):
                        pub_date = pub_date.date()
                    else:
                        pub_date = datetime.fromisoformat(str(pub_date)[:10]).date()

                    # Filter strictly inside range
                    if from_date <= pub_date <= to_date:
                        news_items.append({
                            "title": article.get("headline", {}).get("main"),
                            "url": article.get("web_url"),
                            "source": "NYTimes",
                            "date": str(article.get("pub_date")),
                            "content": None
                        })

            year += 1

        return news_items

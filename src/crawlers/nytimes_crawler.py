from .base import Crawler
from pynytimes import NYTAPI
from datetime import date, datetime, timezone
from tqdm import tqdm

class NYTimesCrawler(Crawler):

    def __init__(self, api_key):
        super().__init__(api_key)
        self.client = NYTAPI(api_key, parse_dates=True)

    def fetch_news(self, from_date=None, to_date=None):
        if from_date is None:
            from_date = date.today().replace(month=1, day=1)
        if to_date is None:
            to_date = date.today()

        if isinstance(from_date, str):
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        if isinstance(to_date, str):
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

        news_items = []

        year = from_date.year
        while year <= to_date.year:
            start_month = from_date.month if year == from_date.year else 1
            end_month = to_date.month if year == to_date.year else 12

            for month in tqdm(range(start_month, end_month + 1), desc=f"NYTimes {year}"):
                archive_data = self.client.archive_metadata(date=date(year, month, 1))

                for article in archive_data:
                    pub_date = article.get("pub_date")
                    if isinstance(pub_date, datetime):
                        pub_date_utc = pub_date.astimezone(timezone.utc)
                    else:
                        pub_date_utc = datetime.fromisoformat(str(pub_date)[:19]).astimezone(timezone.utc)

                    pub_date_str = pub_date_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

                    if from_date <= pub_date_utc.date() <= to_date:
                        news_items.append({
                            "title": article.get("headline", {}).get("main"),
                            "url": article.get("web_url"),
                            "source": "NYTimes",
                            "date": pub_date_str
                        })

            year += 1

        return news_items

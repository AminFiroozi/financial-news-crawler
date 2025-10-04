from .base import Crawler
from pynytimes import NYTAPI
from datetime import date, datetime, timezone
from tqdm import tqdm
import os
import json
import re

class NYTimesCrawler(Crawler):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.client = NYTAPI(api_key, parse_dates=True)

    def _save_item_to_json(self, item):
        """Saves a single raw NYT API article dictionary to a JSON file in the temp directory."""
        temp_dir = "temp"
        # Ensure the temp directory exists
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # NYT Archive articles use '_id' (e.g., 'nyt://article/...')
        item_id = item.get("_id", f"no-id-{datetime.now().strftime('%Y%m%d%H%M%S%f')}")
        
        # Clean up the ID to be a valid filename by replacing non-word characters with underscores
        safe_id = re.sub(r'[^\w-]', '_', item_id)
        filename = os.path.join(temp_dir, f"nyt_{safe_id}.json")

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(item, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving raw NYT item {item_id} to file: {e}")
    
    def fetch_news(self, sections=['business', 'politics', 'your money', 'world', 'technology'], from_date=None, to_date=None):
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
                    # print(article)
                    # break
                    self._save_item_to_json(article)
                    pub_date = article.get("pub_date")
                    if isinstance(pub_date, datetime):
                        pub_date_utc = pub_date.astimezone(timezone.utc)
                    else:
                        pub_date_utc = datetime.fromisoformat(str(pub_date)[:19]).astimezone(timezone.utc)

                    pub_date_str = pub_date_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

                    if from_date <= pub_date_utc.date() <= to_date:
                        if any(section in article.get('section_name').lower() for section in sections):
                            news_items.append({
                                "title": article.get("headline", {}).get("main"),
                                "url": article.get("web_url"),
                                "source": "NYTimes",
                                "date": pub_date_str
                            })

            year += 1

        return news_items

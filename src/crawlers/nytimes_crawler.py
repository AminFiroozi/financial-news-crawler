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

    # --- NEW HELPER METHOD FOR CATEGORY MAPPING ---
    def _map_nytimes_section_to_category(self, section_name):
        """
        Maps the NYT's section name to a standard category name.
        """
        if not section_name:
            return "General"
        
        section_name_lower = section_name.lower()
        
        # Define specific financial/economic categories
        if section_name_lower in ['business', 'dealbook', 'your money', 'economy', 'financial']:
            return "Finance & Business"
        elif section_name_lower in ['politics', 'us', 'world']:
            return "Politics & World"
        elif section_name_lower in ['technology', 'tech', 'science']:
            return "Technology"
        elif section_name_lower in ['culture', 'arts', 'sports', 'style']:
            return "General"
        else:
            return "General" # Default category
    
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
                
                # Check date constraints for NYT Archive API
                # The NYT Archive API only allows retrieving up to the current month.
                current_date = date(year, month, 1)
                if current_date.year > date.today().year or (current_date.year == date.today().year and current_date.month > date.today().month):
                    # Skip fetching future months
                    continue

                archive_data = self.client.archive_metadata(date=current_date)

                for article in archive_data:
                    # print(article)
                    # self._save_item_to_json(article) # Uncomment this if you want to save the raw JSON
                    
                    pub_date = article.get("pub_date")
                    if isinstance(pub_date, datetime):
                        pub_date_utc = pub_date.astimezone(timezone.utc)
                    else:
                        try:
                            # Attempt to parse as ISO 8601 string, often truncated
                            pub_date_utc = datetime.fromisoformat(str(pub_date)[:19]).astimezone(timezone.utc)
                        except:
                            # Fallback if date parsing fails
                            continue 

                    pub_date_str = pub_date_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
                    section_name = article.get('section_name')

                    if from_date <= pub_date_utc.date() <= to_date:
                        # Ensure we check the article's section_name, not just if the sections array has a match
                        if section_name and any(section in section_name.lower() for section in sections):
                            
                            # --- MODIFICATION: ADDED CATEGORY COLUMN ---
                            category = self._map_nytimes_section_to_category(section_name)
                            
                            # The 'lead_paragraph' field is often the closest thing to 'content' in the archive metadata
                            content_snippet = article.get("lead_paragraph")
                            
                            news_items.append({
                                "title": article.get("headline", {}).get("main"),
                                "url": article.get("web_url"),
                                "source": "NYTimes",
                                "date": pub_date_str,
                                "content": content_snippet, # Using lead_paragraph as content
                                "category": category # New column added
                            })

            year += 1

        return news_items
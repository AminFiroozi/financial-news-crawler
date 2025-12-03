# src/crawlers/guardian_crawler.py

from .base import Crawler
from datetime import datetime, timedelta
from tqdm import tqdm
from time import sleep
import json
import os

class GuardianCrawler(Crawler):

    BASE_URL = "https://content.guardianapis.com/search"
    
    # New helper method to save individual items
    def _save_item_to_json(self, item):
        """Saves a single raw Guardian API item dictionary to a JSON file."""
        temp_dir = "temp"
        # Ensure the temp directory exists
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Use the article ID (a unique identifier) to create a unique filename
        item_id = item.get("id", f"no-id-{datetime.now().strftime('%Y%m%d%H%M%S%f')}")
        # Clean up the ID to be a valid filename
        filename = os.path.join(temp_dir, f"{item_id.replace('/', '_')}.json")

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(item, f, ensure_ascii=False, indent=4)
            # You can remove this print if you want less output, but it confirms the save
            # print(f"Saved raw item to: {filename}") 
        except Exception as e:
            print(f"Error saving raw item {item_id} to file: {e}")

    # --- NEW HELPER METHOD FOR CATEGORY MAPPING ---
    def _map_guardian_section_to_category(self, section_name):
        """
        Maps the Guardian's section name to a standard category name.
        """
        if not section_name:
            return "General"
        
        section_name_lower = section_name.lower()
        
        # Define specific financial/economic categories
        if section_name_lower in ['business', 'money', 'economy', 'financial']:
            return "Finance & Business"
        elif section_name_lower in ['politics', 'government', 'world news']:
            return "Politics & World"
        elif section_name_lower in ['technology', 'tech']:
            return "Technology"
        elif section_name_lower in ['sport', 'culture', 'life and style']:
            return "General"
        else:
            return "General" # Default category

    def fetch_news(self, keyword=None, sections=['business', 'politics', 'money', 'world news', 'technology'], from_date=None, to_date=None):
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

            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # First request to get total pages
                    data = self.get_json(self.BASE_URL, params=params)
                    response = data.get("response", {})
                    total_pages = response.get("pages", 1)
                    break  # success, exit retry loop
                except Exception as e:
                    print(f"Error fetching {day_str}, attempt {attempt+1}: {e}")
                    sleep(2)  # wait before retry
            else:
                print(f"Skipping {day_str} after {max_retries} failed attempts.")
                continue  # skip to next day

            for page in range(1, total_pages + 1):
                params["page"] = page
                try:
                    data = self.get_json(self.BASE_URL, params=params)
                    results = data.get("response", {}).get("results", [])
                except Exception as e:
                    print(f"Error fetching page {page} for {day_str}: {e}")
                    continue  # skip this page

                for item in results:
                    # self._save_item_to_json(item) 
                    section_name = item.get("sectionName")
                    
                    if (section_name and section_name.lower() in sections):
                        # --- MODIFICATION: ADDED CATEGORY COLUMN ---
                        category = self._map_guardian_section_to_category(section_name)
                        
                        all_news.append({
                            "title": item.get("webTitle"),
                            "url": item.get("webUrl"),
                            "source": "Guardian",
                            "date": item.get("webPublicationDate"),
                            "content": None,
                            "category": category # New column added
                        })
                        # print(all_news[-1])

        return all_news
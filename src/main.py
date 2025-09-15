# src/main.py

import argparse
from crawlers.guardian_crawler import GuardianCrawler
from config import GUARDIAN_API_KEY

def run_all(keyword=None, from_date=None, to_date=None):
    all_news = []

    guardian = GuardianCrawler(api_key=GUARDIAN_API_KEY)
    all_news.extend(guardian.fetch_news(keyword=keyword, from_date=from_date, to_date=to_date))
    
    print(f"Fetched {len(all_news)} articles")
    for news in all_news:
        print(f"{news['date']} | {news['title']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Guardian news crawler for a keyword and date range.")
    parser.add_argument("--keyword", type=str, help="Keyword to search for in news")
    parser.add_argument("--from_date", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--to_date", type=str, help="End date in YYYY-MM-DD format")

    args = parser.parse_args()
    
    run_all(keyword=args.keyword, from_date=args.from_date, to_date=args.to_date)

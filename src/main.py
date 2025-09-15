# src/main.py

import argparse
from crawlers.guardian_crawler import GuardianCrawler
from config import GUARDIAN_API_KEY
from parsers.parser import normalize_news_list
from storage.storage import save_news

def run_all(keyword=None, from_date=None, to_date=None, file_path="guardian_news.csv"):
    # 1. Fetch news from Guardian
    guardian = GuardianCrawler(api_key=GUARDIAN_API_KEY)
    raw_news = guardian.fetch_news(keyword=keyword, from_date=from_date, to_date=to_date)

    # 2. Normalize news using parser
    news = normalize_news_list(raw_news, source="Guardian")

    # 3. Save news to CSV
    save_news(news, file_path=file_path)

    # 4. Optional: print results
    print(f"Fetched and saved {len(news)} articles to {file_path}")
    for item in news:
        print(f"{item['date']} | {item['title']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Guardian news crawler for a keyword and date range.")
    parser.add_argument("--keyword", type=str, help="Keyword to search for in news")
    parser.add_argument("--from_date", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--to_date", type=str, help="End date in YYYY-MM-DD format")
    parser.add_argument("--file", type=str, default="guardian_news.csv", help="Path to save CSV file")

    args = parser.parse_args()

    run_all(keyword=args.keyword, from_date=args.from_date, to_date=args.to_date, file_path=args.file)
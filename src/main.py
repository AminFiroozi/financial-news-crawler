# src/main.py

import argparse
from crawlers.guardian_crawler import GuardianCrawler
from crawlers.nytimes_crawler import NYTimesCrawler
from config import GUARDIAN_API_KEY, NYTIMES_API_KEY
from parsers.parser import normalize_news_list
from storage.storage import save_news


def run_all(keyword=None, from_date=None, to_date=None, file_path="all_news.csv"):
    all_news = []

    # --- Guardian ---
    guardian = GuardianCrawler(api_key=GUARDIAN_API_KEY)
    raw_guardian = guardian.fetch_news(keyword=keyword, from_date=from_date, to_date=to_date)
    guardian_news = normalize_news_list(raw_guardian, source="Guardian")
    all_news.extend(guardian_news)

    # --- NY Times ---
    nyt = NYTimesCrawler(api_key=NYTIMES_API_KEY)
    raw_nyt = nyt.fetch_news(from_date=from_date, to_date=to_date)
    nyt_news = normalize_news_list(raw_nyt, source="NYTimes")
    all_news.extend(nyt_news)

    # --- Save merged results ---
    save_news(all_news, file_path=file_path)

    # --- Optional print preview ---
    print(f"Fetched and saved {len(all_news)} total articles to {file_path}")
    for item in all_news[:10]:  # print first 10 only
        print(f"[{item['source']}] {item['date']} | {item['title']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Guardian + NYT crawlers and merge results.")
    parser.add_argument("--keyword", type=str, help="Keyword to search for in Guardian (NYT ignores this)")
    parser.add_argument("--from_date", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--to_date", type=str, help="End date in YYYY-MM-DD format")
    parser.add_argument("--file", type=str, default="all_news.csv", help="Path to save merged CSV file")

    args = parser.parse_args()

    run_all(keyword=args.keyword, from_date=args.from_date, to_date=args.to_date, file_path=args.file)

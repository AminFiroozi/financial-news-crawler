# src/main.py

import argparse
from crawlers.guardian_crawler import GuardianCrawler
from crawlers.nytimes_crawler import NYTimesCrawler
from config import GUARDIAN_API_KEY, NYTIMES_API_KEY
from parsers.parser import normalize_news_list
from storage.storage import save_news
from storage.aggregate import aggregate_news
from storage.plot_news import plot_news_counts


def run_all(keyword=None, from_date=None, to_date=None, file_path="all_news.csv", first_source=None):
    all_news = []
    
    # --- Define the crawling order based on the 'first_source' argument ---
    source_order = ["NYTimes", "Guardian"]
    if first_source and first_source.lower() == "guardian":
        source_order = ["Guardian", "NYTimes"]
    elif first_source and first_source.lower() == "nytimes":
        source_order = ["NYTimes", "Guardian"]
        
    print(f"Crawler Order: {source_order[0]} -> {source_order[1]}")
    print("-" * 30)

    # --- Crawler Logic Function ---
    def fetch_and_normalize(source_name, keyword, from_date, to_date):
        if source_name == "NYTimes":
            print("Starting NYTimes crawl...")
            nyt = NYTimesCrawler(api_key=NYTIMES_API_KEY)
            # NYT crawler currently ignores keyword argument in fetch_news
            raw_nyt = nyt.fetch_news(from_date=from_date, to_date=to_date)
            return normalize_news_list(raw_nyt, source="NYTimes")
        
        elif source_name == "Guardian":
            print("Starting Guardian crawl...")
            guardian = GuardianCrawler(api_key=GUARDIAN_API_KEY)
            raw_guardian = guardian.fetch_news(keyword=keyword, from_date=from_date, to_date=to_date)
            return normalize_news_list(raw_guardian, source="Guardian")
        
        return []

    # --- Execute the crawl based on the determined order ---
    for source in source_order:
        news_data = fetch_and_normalize(source, keyword, from_date, to_date)
        all_news.extend(news_data)

    # --- Save merged results ---
    save_news(all_news, file_path=file_path)

    # --- Optional print preview ---
    print("\n" + "="*40)
    print(f"Fetched and saved {len(all_news)} total articles to {file_path}")
    print("="*40)
    for item in all_news[:10]:  # print first 10 only
        # Print the new 'category' column to show the change works
        print(f"[{item['source']}] [{item.get('category', 'N/A')}] {item['date'][:10]} | {item['title'][:70]}...")
        
    aggregated = aggregate_news(all_news)
    # Save plots
    plot_news_counts(aggregated, output_dir="plots")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Guardian + NYT crawlers and merge results.")
    parser.add_argument("--keyword", type=str, help="Keyword to search for in Guardian (NYT ignores this)")
    parser.add_argument("--from_date", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--to_date", type=str, help="End date in YYYY-MM-DD format")
    parser.add_argument("--file", type=str, default="all_news.csv", help="Path to save merged CSV file")
    
    # --- MODIFICATION: New argument for source order ---
    parser.add_argument(
        "--first_source", 
        type=str, 
        choices=["Guardian", "NYTimes"],
        default="NYTimes",
        help="Specify which news source to fetch first (Guardian or NYTimes). Default is NYTimes."
    )

    args = parser.parse_args()

    run_all(
        keyword=args.keyword, 
        from_date=args.from_date, 
        to_date=args.to_date, 
        file_path=args.file,
        first_source=args.first_source # Pass the new argument
    )
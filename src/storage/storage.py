# src/storage/storage.py

import pandas as pd

def save_news(news_list, file_path="news.csv"):
    """
    Save news list to CSV file.
    """
    if not news_list:
        print("No news to save.")
        return

    df = pd.DataFrame(news_list)
    df.to_csv(file_path, index=False)
    print(f"Saved {len(news_list)} articles to {file_path}")

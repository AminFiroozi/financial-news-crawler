# src/storage/aggregate.py
import pandas as pd

def aggregate_news(news_list):
    if not news_list:
        return {}

    df = pd.DataFrame(news_list)
    df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce')
    df = df.dropna(subset=['date'])

    # Daily
    daily_counts = df.groupby(df['date'].dt.date).size()

    # Weekly
    weekly_counts_raw = df.groupby(df['date'].dt.to_period('W')).size()
    weekly_counts = pd.Series(
        data=weekly_counts_raw.values,
        index=weekly_counts_raw.index.to_timestamp().date
    )

    # Monthly
    monthly_counts_raw = df.groupby(df['date'].dt.to_period('M')).size()
    monthly_counts = pd.Series(
        data=monthly_counts_raw.values,
        index=monthly_counts_raw.index.to_timestamp().date
    )

    # Per source
    per_source = {}
    for source in df['source'].unique():
        src_df = df[df['source'] == source]

        daily = src_df.groupby(src_df['date'].dt.date).size()

        weekly_raw = src_df.groupby(src_df['date'].dt.to_period('W')).size()
        weekly = pd.Series(data=weekly_raw.values, index=weekly_raw.index.to_timestamp().date)

        monthly_raw = src_df.groupby(src_df['date'].dt.to_period('M')).size()
        monthly = pd.Series(data=monthly_raw.values, index=monthly_raw.index.to_timestamp().date)

        per_source[source] = {"daily": daily, "weekly": weekly, "monthly": monthly}

    return {"overall": {"daily": daily_counts, "weekly": weekly_counts, "monthly": monthly_counts},
            "per_source": per_source}

# src/storage/plot_news.py
import matplotlib.pyplot as plt
import os

def plot_news_counts(aggregated, output_dir="plots"):
    """
    Plot news counts and save figures.
    :param aggregated: output of aggregate_news()
    :param output_dir: folder to save images
    """
    os.makedirs(output_dir, exist_ok=True)

    # --- Overall plots ---
    for period in ["daily", "weekly", "monthly"]:
        counts = aggregated['overall'][period].sort_index()
        plt.figure(figsize=(12, 6))
        counts.plot(kind='bar' if period=='weekly' else 'line')
        plt.title(f"Overall news counts per {period}")
        plt.xlabel(period.capitalize())
        plt.ylabel("Number of articles")
        plt.tight_layout()
        file_path = os.path.join(output_dir, f"overall_{period}.png")
        plt.savefig(file_path)
        plt.close()
        print(f"Saved plot: {file_path}")

    # --- Per source plots ---
    for source, data in aggregated['per_source'].items():
        for period in ["daily", "weekly", "monthly"]:
            counts = data[period].sort_index()
            plt.figure(figsize=(12, 6))
            counts.plot(kind='bar' if period=='weekly' else 'line')
            plt.title(f"{source} news counts per {period}")
            plt.xlabel(period.capitalize())
            plt.ylabel("Number of articles")
            plt.tight_layout()
            file_path = os.path.join(output_dir, f"{source}_{period}.png")
            plt.savefig(file_path)
            plt.close()
            print(f"Saved plot: {file_path}")

from crawlers.guardian_crawler import GuardianCrawler
from config import GUARDIAN_API_KEY

def run_all():
    all_news = []

    guardian = GuardianCrawler(api_key=GUARDIAN_API_KEY)
    all_news.extend(guardian.fetch_news(keyword="Tesla"))
    
    print(all_news)

if __name__ == "__main__":
    run_all()

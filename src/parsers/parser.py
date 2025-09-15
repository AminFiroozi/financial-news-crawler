# src/parsers/parser.py

def normalize_news_item(item, source):
    """
    Ensure all news items have the same fields.
    """
    return {
        "title": item.get("title") or item.get("webTitle") or item.get("headline"),
        "url": item.get("url") or item.get("webUrl") or item.get("web_url"),
        "source": source,
        "date": item.get("date") or item.get("webPublicationDate") or item.get("pub_date"),
        "content": item.get("content") or item.get("abstract") or "",
    }

def normalize_news_list(news_list, source):
    return [normalize_news_item(item, source) for item in news_list]

import json
import os
import feedparser
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SEEN_URLS_FILE = "seen_urls.json"

def load_seen_urls():
    if os.path.exists(SEEN_URLS_FILE):
        with open(SEEN_URLS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_seen_urls(urls):
    with open(SEEN_URLS_FILE, "w") as f:
        json.dump(list(urls), f, indent=2)

def mark_as_seen(articles):
    seen = load_seen_urls()
    for article in articles:
        seen.add(article["url"])
    save_seen_urls(seen)

def fetch_rss_articles(feed_url, source_name, max_results=15):
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        for entry in feed.entries[:max_results]:
            title = entry.get("title", "")
            summary = entry.get("summary", entry.get("description", ""))
            url = entry.get("link", "")
            if title and url:
                articles.append({
                    "title": title,
                    "abstract": summary or title,
                    "url": url,
                    "source": source_name
                })
        print(f"Found {len(articles)} articles from {source_name}.")
        return articles
    except Exception as e:
        print(f"Error fetching {source_name}: {e}")
        return []


def fetch_all_articles(days_back=7):
    all_articles = []

    # Physician-specific finance blogs
    all_articles += fetch_rss_articles(
        "https://www.whitecoatinvestor.com/feed/",
        "White Coat Investor"
    )
    all_articles += fetch_rss_articles(
        "https://www.physicianonfire.com/feed/",
        "Physician on FIRE"
    )

    # General personal finance (high quality)
    all_articles += fetch_rss_articles(
        "https://www.bogleheads.org/blog/feed/",
        "Bogleheads"
    )
    all_articles += fetch_rss_articles(
        "https://thefinancebuff.com/feed",
        "The Finance Buff"
    )
    all_articles += fetch_rss_articles(
        "https://www.mrmoneymustache.com/feed/",
        "Mr. Money Mustache"
    )

    # Market and economic news
    all_articles += fetch_rss_articles(
        "https://feeds.marketwatch.com/marketwatch/topstories/",
        "MarketWatch"
    )
    all_articles += fetch_rss_articles(
        "https://www.nerdwallet.com/blog/feed/",
        "NerdWallet"
    )

    print(f"\nTotal articles collected: {len(all_articles)}")

    seen = load_seen_urls()
    fresh = [a for a in all_articles if a["url"] not in seen]
    print(f"Fresh unseen articles: {len(fresh)} (filtered out {len(all_articles) - len(fresh)} already seen)")

    return fresh


if __name__ == "__main__":
    articles = fetch_all_articles(days_back=7)
    print(f"\nSaved {len(articles)} articles")
    if articles:
        for a in articles[:5]:
            print(f"  [{a['source']}] {a['title'][:70]}...")

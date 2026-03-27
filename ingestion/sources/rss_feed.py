import feedparser

RSS_FEEDS = [
    # India Business 
    "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
    "https://www.livemint.com/rss/news",
    "https://www.business-standard.com/rss/home_page_top_stories.rss",

    # RBI / Policy 
    "https://www.rbi.org.in/scripts/rss.aspx",

    # Global Markets 
    "https://www.reuters.com/business/rss",
    "https://www.reuters.com/markets/rss",

    # Commodities / Energy 
    "https://oilprice.com/rss/main",

    # Trade / Policy 
    "https://www.wto.org/rss/news_e.xml",

    # Shipping / Logistics 
    "https://www.hellenicshippingnews.com/feed/",
]

# Global risk keywords — broad first-pass filter
KEYWORDS = [
    "oil", "energy", "sanctions", "trade", "tariff",
    "shipping", "supply chain", "inflation", "interest rates",
    "currency", "exports", "imports", "commodities",
    "rupee", "rbi", "india", "crude", "freight", "geopolit",
]


def fetch_rss_news(max_per_feed: int = 10) -> list[dict]:
    articles = []

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)

            if feed.bozo:
                print(f"[RSS] Warning: malformed feed at {url}")

            for entry in feed.entries[:max_per_feed]:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()

                if not title or not link:
                    continue

                articles.append({
                    "title": title,
                    "summary": entry.get("summary", "").strip(),
                    "link": link,
                    "published": entry.get("published", ""),
                    "source": url,
                })

        except Exception as e:
            print(f"[RSS] Failed to fetch {url}: {e}")
            continue

    return articles


def filter_relevant_articles(articles: list[dict]) -> list[dict]:
    """
    Broad first-pass filter — keeps articles mentioning
    at least one risk keyword. Narrative agent does the
    deeper company-specific filtering after this.
    """
    filtered = []

    for article in articles:
        text = (article["title"] + " " + article["summary"]).lower()
        if any(keyword in text for keyword in KEYWORDS):
            filtered.append(article)

    return filtered


def fetch_and_filter_news(max_per_feed: int = 10) -> list[dict]:
    """
    Convenience function — fetch + filter in one call.
    Use this in your pipeline instead of calling both separately.
    """
    articles = fetch_rss_news(max_per_feed)
    filtered = filter_relevant_articles(articles)
    print(f"[RSS] Fetched {len(articles)} articles, {len(filtered)} passed keyword filter")
    return filtered
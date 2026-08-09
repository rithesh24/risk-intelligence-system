import time
import socket
import feedparser

RSS_FEEDS = [
    # India Business
    "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
    "https://www.livemint.com/rss/news",
    "https://www.business-standard.com/rss/home_page_top_stories.rss",
    "https://www.moneycontrol.com/rss/business.xml",

    # RBI / Policy — rbi.org.in's own feed has been discontinued; Google News
    # aggregates the same coverage from live publishers instead
    "https://news.google.com/rss/search?q=RBI+monetary+policy&hl=en-IN&gl=IN&ceid=IN:en",

    # Global Markets — reuters.com/*/rss now 401s (Reuters retired public RSS)
    "http://feeds.bbci.co.uk/news/business/rss.xml",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://finance.yahoo.com/news/rssindex",

    # Commodities / Energy
    "https://oilprice.com/rss/main",

    # Trade / Policy — wto.org's feed now redirects to a non-RSS page
    "https://news.google.com/rss/search?q=WTO+trade+tariff&hl=en&gl=US&ceid=US:en",

    # Geopolitics
    "https://news.google.com/rss/search?q=geopolitics+sanctions+supply+chain&hl=en&gl=US&ceid=US:en",
    "https://www.aljazeera.com/xml/rss/all.xml",

    # Shipping / Logistics
    "https://www.hellenicshippingnews.com/feed/",
]

# Some publishers (e.g. Business Standard) block feedparser's default UA with a 403
_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Global risk keywords — broad first-pass filter
KEYWORDS = [
    "oil", "energy", "sanctions", "trade", "tariff",
    "shipping", "supply chain", "inflation", "interest rates",
    "currency", "exports", "imports", "commodities",
    "rupee", "rbi", "india", "crude", "freight", "geopolit",
]


def fetch_rss_news(max_per_feed: int = 10) -> list[dict]:
    articles = []

    socket.setdefaulttimeout(5)  # feedparser has no per-call timeout arg
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url, agent=_USER_AGENT)

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


_NEWS_CACHE_TTL_SECONDS = 600  # ponytail: global in-memory cache, move to Redis if scaled to multiple workers
_news_cache: dict[str, tuple[float, list[dict]]] = {}


def fetch_and_filter_news(max_per_feed: int = 10) -> list[dict]:
    """
    Convenience function — fetch + filter in one call, cached for
    _NEWS_CACHE_TTL_SECONDS so repeated analyze requests don't re-hit
    all RSS feeds every time.
    """
    cached = _news_cache.get("filtered")
    if cached and (time.time() - cached[0]) < _NEWS_CACHE_TTL_SECONDS:
        return cached[1]

    articles = fetch_rss_news(max_per_feed)
    filtered = filter_relevant_articles(articles)
    print(f"[RSS] Fetched {len(articles)} articles, {len(filtered)} passed keyword filter")
    _news_cache["filtered"] = (time.time(), filtered)
    return filtered
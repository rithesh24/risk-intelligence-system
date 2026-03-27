from events.models.news_event import NewsEvent


def build_news_events(articles: list[dict]) -> list[NewsEvent]:
    events = []

    for article in articles:
        try:
            event = NewsEvent(
                title=article["title"],
                summary=article.get("summary", ""),
                source=article.get("source", ""),
                link=article.get("link", ""),
                published=article.get("published", ""),  
            )
            events.append(event)
        except (KeyError, ValueError) as e:
            print(f"[EventBuilder] Skipping malformed article: {e}")
            continue

    return events
import random
import feedparser
import requests
from typing import List
from config.config import SERPER_API_KEY

def fetch_rss_headlines(feeds: List[str], max_items: int = 15) -> List[dict]:
    headlines = []
    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:
                headlines.append({
                    "title":   entry.get("title", ""),
                    "summary": entry.get("summary", "")[:300],
                    "source":  feed.feed.get("title", feed_url),
                })
        except Exception as e:
            print(f"  [WARN] RSS fetch failed {feed_url}: {e}")
    random.shuffle(headlines)
    return headlines[:max_items]

def search_trending_topics(queries: List[str]) -> List[dict]:
    if not SERPER_API_KEY:
        return []
    results = []
    for query in queries[:2]:
        try:
            resp = requests.post(
                "https://google.serper.dev/news",
                headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
                json={"q": query, "num": 5},
                timeout=10,
            )
            for r in resp.json().get("news", []):
                results.append({
                    "title":   r["title"],
                    "summary": r.get("snippet", ""),
                    "source":  r.get("source", ""),
                })
        except Exception as e:
            print(f"  [WARN] Serper failed for '{query}': {e}")
    return results

def gather_research(topic_config: dict) -> str:
    print(f"🔍 Researching: {topic_config['label']}...")
    headlines = fetch_rss_headlines(topic_config["rss_feeds"])
    web_results = search_trending_topics(topic_config["serper_queries"])
    all_items = (web_results + headlines)[:20]

    if not all_items:
        return f"Focus on latest developments in: {topic_config['label']}."

    brief = f"TRENDING HEADLINES — {topic_config['name'].upper()}:\n\n"
    for i, item in enumerate(all_items, 1):
        brief += f"{i}. [{item['source']}] {item['title']}\n"
        if item.get("summary"):
            brief += f"   {item['summary'][:200]}\n"
        brief += "\n"
    return brief

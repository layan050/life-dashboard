import feedparser
from plugins.base import BasePlugin

class SubstackPlugin(BasePlugin):
    def __init__(self, feed_url: str):
        super().__init__("substack")
        self.feed_url = feed_url

    def fetch(self):
        feed = feedparser.parse(self.feed_url)
        if feed.entries:
            latest = feed.entries[0]
            return {
                "title": "📚 Substack",
                "category": "آخر المقالات",
                "item_title": latest.title,
                "link": latest.link,
                "published": latest.get("published", "")[:16]
            }
        return {"title": "📚 Substack", "status_text": "لا توجد منشورات جديدة"}
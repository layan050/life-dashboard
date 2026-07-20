import feedparser
from plugins.base import BasePlugin

class YoutubePlugin(BasePlugin):
    def __init__(self, channel_id: str):
        super().__init__("youtube")
        self.feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

    def fetch(self):
        feed = feedparser.parse(self.feed_url)
        if feed.entries:
            latest = feed.entries[0]
            return {
                "title": "🎥 YouTube",
                "category": "شاهدت/نشرت مؤخراً",
                "item_title": latest.title,
                "link": latest.link
            }
        return {"title": "🎥 YouTube", "status_text": "لا توجد فيديوهات"}
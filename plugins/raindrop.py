import requests
from plugins.base import BasePlugin

class RaindropPlugin(BasePlugin):
    def __init__(self, token: str, collection_id: str = "0"):
        super().__init__("raindrop")
        self.token = token
        self.collection_id = collection_id

    def fetch(self):
        if not self.token:
            return {"title": "🔖 Raindrop.io", "status_text": "غير مفعل (رمز Access Token مفقود)"}

        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"https://api.raindrop.io/v1/raindrops/{self.collection_id}?perpage=1"
        
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            items = res.json().get("items", [])
            if items:
                latest = items[0]
                return {
                    "title": "🔖 المفضلات الأخيرة",
                    "category": "أضفت مرجعاً",
                    "item_title": latest.get("title"),
                    "link": latest.get("link"),
                    "domain": latest.get("domain")
                }
        return {"title": "🔖 Raindrop.io", "status_text": "لا توجد عناصر محفوظة"}
import requests
from plugins.base import BasePlugin

class GithubPlugin(BasePlugin):
    def __init__(self, username: str):
        super().__init__("github")
        self.username = username

    def fetch(self):
        url = f"https://api.github.com/users/{self.username}/events/public"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            events = res.json()
            if events:
                latest = events[0]
                event_type = latest.get("type")
                repo_name = latest.get("repo", {}).get("name")
                return {
                    "title": "💻 GitHub",
                    "category": "النشاط البرمجي",
                    "status_text": f"نشاط ({event_type}) في {repo_name}",
                    "link": f"https://github.com/{repo_name}"
                }
        return {"title": "💻 GitHub", "status_text": "لا يوجد نشاط برمي حديث"}
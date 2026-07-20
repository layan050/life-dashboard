import requests

class SubstackPlugin:
    def __init__(self, username):
        self.name = "substack"
        self.username = username

    def run(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            # 1. جلب ID المستخدم
            profile_url = f"https://substack.com/api/v1/user/{self.username}/public_profile"
            res = requests.get(profile_url, headers=headers, timeout=10)
            
            if res.status_code != 200:
                return {"status": "error", "message": "Substack profile not found"}
                
            user_id = res.json().get("id")
            if not user_id:
                return {"status": "error", "message": "User ID not found"}

            # 2. جلب خلاصة النشاطات و الـ Restack
            feed_url = f"https://substack.com/api/v1/reader/feed/profile/{user_id}"
            feed_res = requests.get(feed_url, headers=headers, timeout=10)
            
            if feed_res.status_code == 200:
                items = feed_res.json().get("items", [])
                for item in items:
                    post = item.get("post") or (item.get("comment", {}) or {}).get("post")
                    if post:
                        return {
                            "status": "success",
                            "data": {
                                "title": "📚 Substack",
                                "item_title": post.get("title"),
                                "link": post.get("canonical_url")
                            }
                        }

            return {
                "status": "success",
                "data": {
                    "title": "📚 Substack",
                    "item_title": "لا يوجد Restack مؤخراً",
                    "link": f"https://substack.com/@{self.username}"
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
import requests
from plugins.base import BasePlugin

class ChessPlugin(BasePlugin):
    def __init__(self, username: str):
        super().__init__("chess")
        self.username = username

    def fetch(self):
        headers = {'User-Agent': 'LifeDashboardBlogger/1.0'}
        
        # جلب الإحصائيات
        stats_res = requests.get(f"https://api.chess.com/pub/player/{self.username}/stats", headers=headers, timeout=10)
        stats = stats_res.json() if stats_res.status_code == 200 else {}
        
        # جلب أحدث المباريات
        games_res = requests.get(f"https://api.chess.com/pub/player/{self.username}/games/latest", headers=headers, timeout=10)
        latest_games = games_res.json().get('games', []) if games_res.status_code == 200 else []
        
        last_game_info = "لا توجد مباريات حديثة"
        if latest_games:
            last_game = latest_games[-1]
            white = last_game['white']['username']
            black = last_game['black']['username']
            is_white = white.lower() == self.username.lower()
            result = last_game['white']['result'] if is_white else last_game['black']['result']
            
            outcome = "✅ فوز" if result == "win" else ("🤝 تعادل" if result in ["agreed", "repetition", "stalemate"] else "❌ خسارة")
            opponent = black if is_white else white
            last_game_info = f"{outcome} ضد {opponent}"

        rapid_rating = stats.get('chess_rapid', {}).get('last', {}).get('rating', 'N/A')

        return {
            "title": "♟️ Chess.com",
            "type": "game",
            "category": "ألعب الآن",
            "rating": f"Rapid {rapid_rating}",
            "status_text": last_game_info,
            "link": f"https://www.chess.com/member/{self.username}"
        }
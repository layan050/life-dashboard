import json
import os
from datetime import datetime

# استيراد الـ Plugins
from plugins.chess import ChessPlugin
from plugins.raindrop import RaindropPlugin
from plugins.substack import SubstackPlugin
from plugins.youtube import YoutubePlugin
from plugins.github_activity import GithubPlugin
from plugins.manual_override import ManualPlugin

def build_dashboard():
    # --- ضبط الإعدادات وحساباتك هنا ---
    CHESS_USERNAME = "YourChessUsername"
    GITHUB_USERNAME = "YourGithubUsername"
    SUBSTACK_FEED = "https://yourblog.substack.com/feed"
    YOUTUBE_CHANNEL_ID = "UCxxxxxxxxxxxx"  # ضع Channel ID لقناتك أو قناتك المفضل
    RAINDROP_TOKEN = os.getenv("RAINDROP_TOKEN", "") # يُجلب من خيارات الأمان في GitHub

    # تسجيل جميع الإضافات
    plugins = [
        ChessPlugin(CHESS_USERNAME),
        GithubPlugin(GITHUB_USERNAME),
        SubstackPlugin(SUBSTACK_FEED),
        YoutubePlugin(YOUTUBE_CHANNEL_ID),
        RaindropPlugin(RAINDROP_TOKEN),
        ManualPlugin("data/manual_data.json")
    ]

    dashboard_output = {
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "widgets": {}
    }

    # تشغيل كل Plugin بشكل مستقل
    for plugin in plugins:
        print(f"[RUNNING] Plugin: {plugin.name}")
        result = plugin.run()
        dashboard_output["widgets"][plugin.name] = result

    # حفظ النتيجة في ملف JSON واحد
    output_path = "dashboard-data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dashboard_output, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Dashboard generated successfully at {output_path}")

if __name__ == "__main__":
    build_dashboard()
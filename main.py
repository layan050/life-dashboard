import json
import os
from datetime import datetime

# استيراد الـ Plugins المتاحة والفعالة
from plugins.chess import ChessPlugin
from plugins.substack import SubstackPlugin
from plugins.youtube import YoutubePlugin
from plugins.github_activity import GithubPlugin
from plugins.manual_override import ManualPlugin

def build_dashboard():
    # --- ضبط الإعدادات وحساباتك ---
    CHESS_USERNAME = "laayyyaann"
    GITHUB_USERNAME = "layan050"
    
    # اسم مستخدم Substack (بدون رابط وبدون @)
    SUBSTACK_USERNAME = "layann77"  # 👈 تأكدي أن هذا هو يوزر حسابك في سبستاك
    
    YOUTUBE_CHANNEL_ID = "UCAhqkGAhblH3i99fFSCFzDA"

    # تسجيل الإضافات الفعالة
    plugins = [
        ChessPlugin(CHESS_USERNAME),
        GithubPlugin(GITHUB_USERNAME),
        SubstackPlugin(SUBSTACK_USERNAME),
        YoutubePlugin(YOUTUBE_CHANNEL_ID),
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
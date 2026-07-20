from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePlugin(ABC):
    """
    Class قاعدة لجميع الـ Plugins لضمان الحماية والمرونة.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def fetch(self) -> Dict[str, Any]:
        """طريقة جلب البيانات التي يجب تنفيذها في كل Plugin"""
        pass

    def run(self) -> Dict[str, Any]:
        """تغليف عملية الجلب داخل try-except لضمان عدم انهيار بقية المشروع عند حدوث خطأ"""
        try:
            data = self.fetch()
            return {
                "status": "success",
                "data": data
            }
        except Exception as e:
            print(f"[ERROR] Plugin '{self.name}' failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "data": None
            }
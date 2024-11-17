from apk_editor.utils import is_java_installed
from apk_editor.apk import APK

__version__ = "0.1.0"


if not is_java_installed():
    raise RuntimeError("Java is not installed")

__all__ = ["APK"]

from apk_editor.utils import is_java_installed
from apk_editor.smali.smali_utils import SmaliUtils

__version__ = "0.1.2"


if not is_java_installed():
    raise RuntimeError("Java is not installed")

__all__ = ["SmaliUtils"]

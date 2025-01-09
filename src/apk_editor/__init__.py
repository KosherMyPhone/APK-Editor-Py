from apk_editor.smali.smali_utils import SmaliUtils
from apk_editor.utils import is_java_installed

__version__ = "0.1.5"


if not is_java_installed():
    raise RuntimeError("Java is not installed")

__all__ = ["SmaliUtils"]

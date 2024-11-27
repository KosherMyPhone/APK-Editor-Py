from apk_editor.utils import is_java_installed

__version__ = "0.1.2"


if not is_java_installed():
    raise RuntimeError("Java is not installed")

from pathlib import Path

import appdirs

DATA_DIR = Path(appdirs.user_data_dir("apk-editor-py", "KosherMyPhone"))
BINARIES_DIR = DATA_DIR / "binaries"

APKSIGNER = BINARIES_DIR / "apksigner" / "apksigner.jar"


APKEDITOR_VERSION = "1.4.1"
APKEDITOR_RELEASE_URL = f"https://api.github.com/repos/reandroid/apkeditor/releases/tags/V{APKEDITOR_VERSION}"

APKEDITOR = BINARIES_DIR / "apkeditor" / "apkeditor.jar"

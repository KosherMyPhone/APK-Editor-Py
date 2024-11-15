from pathlib import Path
import appdirs

data_dir = Path(appdirs.user_data_dir("apk-editor-py", "KosherMyPhone"))
binaries_dir = data_dir / "binaries"

apkeditor_version = "1.4.1"
apkeditor_release_url = f"https://api.github.com/repos/reandroid/apkeditor/releases/tags/V{apkeditor_version}"

apkeditor = binaries_dir / "apkeditor" / "apkeditor.jar"

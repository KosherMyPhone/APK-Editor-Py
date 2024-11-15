from pathlib import Path
import subprocess
import random
from apk_editor.constants import apkeditor
from tempfile import TemporaryDirectory


class DecompiledAPK:
    def __init__(self, path: Path):
        self.path = path
        self.androidmanifest = self.path / "AndroidManifest.xml.json"


class APK:
    def __init__(self, path: Path):
        self.path = path

    def decompile(self):
        temp_dir = TemporaryDirectory()
        output_dir = Path(temp_dir.name)
        subprocess.run(
            [
                "java",
                "-jar",
                apkeditor,
                "decode",
                "-i",
                self.path,
                "-o",
                output_dir,
                "-t",
                "json",
            ],
            check=True,
            capture_output=True,
        )

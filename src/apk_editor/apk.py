from pathlib import Path
import subprocess
from apk_editor.constants import apkeditor
from tempfile import TemporaryDirectory

from apk_editor.smali import SmaliUtils


class DecompiledAPK:
    def __init__(self, path: Path):
        self.path = path
        self.androidmanifest: Path = self.path / "AndroidManifest.xml.json"
        self.smali_path: Path = self.path / "smali"
        self.smali_utils = SmaliUtils(self)


class APK:
    def __init__(self, path: Path):
        self.path = path
        self.temp_dir: TemporaryDirectory = None

    def decompile(self) -> DecompiledAPK:
        self.temp_dir = TemporaryDirectory()
        output_dir = Path(self.temp_dir.name)
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

        return DecompiledAPK(output_dir)

    def cleanup(self):
        self.temp_dir.cleanup()

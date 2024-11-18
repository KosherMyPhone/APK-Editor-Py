from collections import namedtuple
import json
from pathlib import Path
import subprocess
from apk_editor.constants import apkeditor
from tempfile import TemporaryDirectory


class DecompiledAPK:
    def __init__(self, path: Path):
        self.path = path
        self.androidmanifest: Path = self.path / "AndroidManifest.xml.json"
        self.smali_path: Path = self.path / "smali"


class APK:
    def __init__(self, path: Path):
        self.path = path
        self.temp_dir: TemporaryDirectory = None
        self.decompiled_apk: DecompiledAPK = None

    def decompile(self) -> DecompiledAPK:
        self.temp_dir = TemporaryDirectory()
        output_dir = Path(self.temp_dir.name + "/decompiled")
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

        self.decompiled_apk = DecompiledAPK(output_dir)
        return self.decompiled_apk

    def cleanup(self):
        self.temp_dir.cleanup()


APKInfo = namedtuple(
    "APKInfo",
    [
        "package_name",
        "version_code",
        "version_name",
        "app_name",
        "app_icon_path",
        "application_class",
        "main_activity",
    ],
)


def get_apk_info(apk_path: Path) -> APKInfo:
    get_info_cmd = ["java", "-jar", apkeditor, "info", "-i", apk_path, "-t", "json"]
    result = subprocess.run(get_info_cmd, check=True, capture_output=True)
    results = json.loads(result.stdout)
    res_fmt = {list(d.keys())[0]: list(d.values())[0] for d in results}
    # return res_fmt
    return APKInfo(
        res_fmt["package"],
        res_fmt["VersionCode"],
        res_fmt["VersionName"],
        res_fmt["AppName"],
        res_fmt["AppIcon"],
        res_fmt["application-class"],
        res_fmt["activity-main"],
    )

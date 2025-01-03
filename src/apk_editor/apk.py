from dataclasses import dataclass
import json
import subprocess
from collections import namedtuple
from pathlib import Path
from tempfile import TemporaryDirectory

from apk_editor.constants import APKEDITOR

class DecompiledAPK:
    def __init__(self, path: Path):
        self.path = path
        self.androidmanifest: Path = self.path / "AndroidManifest.xml.json"
        self.resources_arsc: Path = self.path / "resources" / "resources.arsc.json"
        self.smali_path: Path = self.path / "smali"


class APK:
    def __init__(self, path: Path):
        self.path = path
        self.temp_dir: TemporaryDirectory = TemporaryDirectory()
        self.decompiled_apk: DecompiledAPK | None = None

    def decompile(self) -> DecompiledAPK:
        output_dir = Path(self.temp_dir.name + "/decompiled")
        subprocess.run(
            [
                "java",
                "-jar",
                APKEDITOR,
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

    def compile(self):
        if not self.decompiled_apk:
            raise ValueError("APK must be decompiled before compiling")
        output_file = Path(self.temp_dir.name + "/compiled.apk")
        subprocess.run(
            [
                "java",
                "-jar",
                APKEDITOR,
                "build",
                "-i",
                self.decompiled_apk.path,
                "-o",
                output_file,
            ],
            check=True,
            capture_output=True,
        )
        return output_file

    def cleanup(self):
        self.temp_dir.cleanup()

@dataclass
class APKInfo:
    package_name: str
    version_code: str
    version_name: str
    app_name: str
    app_icon_path: str
    application_class: str
    main_activity: str


# APKInfo = namedtuple(
#     "APKInfo",
#     [
#         "package_name",
#         "version_code",
#         "version_name",
#         "app_name",
#         "app_icon_path",
#         "application_class",
#         "main_activity",
#     ],
# )


def get_apk_info(apk_path: Path) -> APKInfo:
    """
    Extract information from an APK file using apkeditor's info command.

    Args:
        apk_path: The path to the APK file.

    Returns:
        An APKInfo tuple containing the package name, version code, version name,
        app name, app icon path, application class, and main activity class.
    """

    get_info_cmd = ["java", "-jar", APKEDITOR, "info", "-i", apk_path, "-t", "json"]
    result = subprocess.run(get_info_cmd, check=True, capture_output=True)
    results = json.loads(result.stdout)
    res_fmt = {list(d.keys())[0]: list(d.values())[0] for d in results}
    # return res_fmt
    return APKInfo(
        res_fmt.get("package", None),
        res_fmt.get("VersionCode", None),
        res_fmt.get("VersionName", None),
        res_fmt.get("AppName", None),
        res_fmt.get("AppIcon", None),
        res_fmt.get("application-class", None),
        res_fmt.get("activity-main", None),
    )

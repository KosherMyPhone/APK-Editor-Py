import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from apk_editor.constants import apkeditor


class DecompiledAPK:
    def __init__(self, path: Path):
        self.path = path
        self.androidmanifest: Path = self.path / "AndroidManifest.xml.json"
        self.smali_path: Path = self.path / "smali"
        self.smali_dir: Path = self.smali_path  # I don't want to make breaking changes. But I want to use dir where appropriate.
        self.res_dir: Path = self.path / "res-json" / "res"
        self.root_dir: Path = self.path / "root"
        self.root_res_dir: Path = self.root_dir / "res"
        self.resources_arsc: Path = self.path / "resources" / "resources.arsc.json"


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

    def compile(self):
        output_file = Path(self.temp_dir.name + "/compiled.apk")
        subprocess.run(
            [
                "java",
                "-jar",
                apkeditor,
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


def get_apk_info(apk_path: Path) -> APKInfo:
    """
    Extract information from an APK file using apkeditor's info command.

    Args:
        apk_path: The path to the APK file.

    Returns:
        An APKInfo tuple containing the package name, version code, version name,
        app name, app icon path, application class, and main activity class.
    """

    get_info_cmd = ["java", "-jar", apkeditor, "info", "-i", apk_path, "-t", "json"]
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

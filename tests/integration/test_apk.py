from pathlib import Path
from zipfile import ZipFile

from apk_editor.apk import APK
from apk_editor.smali import SmaliUtils

apks_dir = Path(__file__).parents[1] / "apks"
test_apk_path = apks_dir / "open_recents.apk"


def test_apk():
    apk = APK(test_apk_path)
    decompiled_apk = apk.decompile()
    assert decompiled_apk.androidmanifest.is_file(), "AndroidManifest.xml not found"
    assert decompiled_apk.smali_path.is_dir(), "smali directory not found"
    smali_utils = SmaliUtils(decompiled_apk)
    main_activity_path = smali_utils.find_activity_or_class(
        "com.duoqin.ai.MainActivity"
    )
    assert main_activity_path.is_file(), "MainActivity not found"
    compiled_apth = apk.compile()
    assert compiled_apth.is_file(), "compiled.apk not found"
    with ZipFile(compiled_apth, "r") as zf:
        assert all(
            file in zf.namelist()
            for file in [
                "AndroidManifest.xml",
                "classes.dex",
                "resources.arsc",
                "res/mipmap-hdpi/ic_launcher.png",
            ]
        ), "APK Not compiled properly"
    apk.cleanup()
    assert Path(apk.temp_dir.name).exists() is False

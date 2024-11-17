from pathlib import Path
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
    apk.cleanup()
    assert Path(apk.temp_dir.name).exists() is False

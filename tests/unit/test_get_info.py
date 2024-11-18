from apk_editor.apk import get_apk_info
from pathlib import Path

apks_dir = Path(__file__).parents[1] / "apks"
test_apk_path = apks_dir / "open_recents.apk"


def test_get_apk_info():
    apk_info = get_apk_info(test_apk_path)
    assert (
        apk_info.package_name == "com.android.cts.UT.recent"
        and apk_info.version_code == 5
        and apk_info.app_name == "Recent apps"
        and apk_info.application_class is None
        and apk_info.main_activity == "com.duoqin.ai.MainActivity"
    )

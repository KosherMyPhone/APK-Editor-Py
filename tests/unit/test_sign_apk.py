import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from apk_editor.constants import APKSIGNER
from apk_editor.sign import SigningKey, sign_apk

apks_dir = Path(__file__).parents[1] / "apks"
keys_dir = Path(__file__).parents[1] / "keys"
pk8_path = keys_dir / "key.pk8"
x509_path = keys_dir / "cert.x509.pem"
test_apk_path = apks_dir / "open_recents.apk"


def test_sign_apk():
    dir = TemporaryDirectory()
    out_path = Path(dir.name + "/signed.apk")
    key = SigningKey(pk8_path=pk8_path, x509_path=x509_path)
    sign_apk(test_apk_path, key, out_path)
    check_cert_cmd = [
        "java",
        "-jar",
        APKSIGNER,
        "verify",
        "--in",
        out_path,
        "--print-certs",
    ]
    result = subprocess.run(check_cert_cmd, check=True, capture_output=True, text=True)
    assert "CN=apk-editor-py" in result.stdout, "Failed to sign APK"
    dir.cleanup()

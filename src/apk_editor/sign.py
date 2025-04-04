import subprocess
from dataclasses import dataclass
from pathlib import Path

from apk_editor.constants import APKSIGNER


@dataclass
class SigningKey:
    pk8_path: Path
    x509_path: Path


def sign_apk(
    apk_path: Path, signing_key: SigningKey, output_path: Path | None = None
) -> None:
    sign_cmd = [
        "java",
        "-jar",
        APKSIGNER,
        "sign",
        "--in",
        apk_path,
        "--key",
        signing_key.pk8_path,
        "--cert",
        signing_key.x509_path,
        "-v4-signing-enabled",
        "false",  # mainly because I dont want that idsig file
    ]

    if output_path:
        sign_cmd += ["--out", output_path]
    subprocess.run(sign_cmd, check=True, capture_output=True)

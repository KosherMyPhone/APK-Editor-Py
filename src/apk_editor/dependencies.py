import argparse
import os
import shutil
import stat
from enum import Enum
from pathlib import Path

import psutil
import requests

from apk_editor.constants import APKEDITOR_RELEASE_URL, APKEDITOR_VERSION, BINARIES_DIR
from apk_editor.logger import logger
from apk_editor.utils import download_file


class ConnectionType(Enum):
    LOCAL = "local"
    REMOTE = "remote"


class DependencyGetter:
    def __init__(self):
        self.deps_dir = BINARIES_DIR
        if not self.deps_dir.is_dir():
            self.deps_dir.mkdir(parents=True)
        else:
            shutil.rmtree(self.deps_dir)
            self.deps_dir.mkdir(parents=True)

    def get_dependencies(self, connection_type: ConnectionType) -> None:
        if not isinstance(connection_type, ConnectionType):
            raise ValueError(f"expected ConnectionType, got {type(connection_type)}")
        if connection_type is ConnectionType.LOCAL:
            self.get_local_deps()
        elif connection_type is ConnectionType.REMOTE:
            self.get_remote_deps()
        for root, dirs, files in self.deps_dir.walk():
            for f in files:
                file = root / f
                if file.is_file() and not file.suffix:  # binary executables
                    current_permissions = stat.S_IMODE(os.stat(file).st_mode)
                    new_permissions = (
                        current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
                    )
                    os.chmod(file, new_permissions)

    def get_local_deps(self):
        # We will look for apkeditordeps.zip in all filesystems
        # Generally I would use all=False, but sometimes someone will not
        # have an external drive etc so he can make his own mount
        # Also, development is done in WSL and all=False doesnt show usb
        # drives we mounted using  `sudo mount -t drvfs X: /mnt/x`
        partitions = psutil.disk_partitions(all=True)
        for partition in partitions:
            deps_zip = Path(partition.mountpoint) / "apkeditordeps.zip"
            if deps_zip.is_file():
                shutil.unpack_archive(deps_zip, self.deps_dir)
                return

        raise FileNotFoundError("could not find local dependencies")

    def get_remote_deps(self):
        with requests.get(APKEDITOR_RELEASE_URL) as r:
            release = r.json()
        for asset in release["assets"]:
            if (
                asset["name"].casefold().startswith("apkeditor")
                and APKEDITOR_VERSION in asset["name"]
                and asset["name"].endswith(".jar")
            ):
                dl_folder = self.deps_dir / "apkeditor"
                dl_folder.parent.mkdir(parents=True, exist_ok=True)
                download_file(
                    asset["browser_download_url"], dl_folder / "apkeditor.jar"
                )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=["local", "remote"])
    args = parser.parse_args()
    logger.info(f"Getting {args.type} dependencies")
    DependencyGetter().get_dependencies(ConnectionType(args.type))
    logger.info("Completed Successfully")


if __name__ == "__main__":
    main()

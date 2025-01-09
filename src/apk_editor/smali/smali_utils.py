from pathlib import Path
from apk_editor.apk import DecompiledAPK


class SmaliUtils:
    def __init__(self, decompiled_apk: DecompiledAPK):
        self.apk = decompiled_apk

    def find_activity_or_class(self, class_name: str) -> Path | None:
        """Find the smali file for the given class name.

        Args:
            class_name (str): The class name to search for.

        Returns:
            Path | None: The path to the smali file if found, None otherwise.
        """
        base_name = class_name.split(".")[-1]
        for root, dirs, files in self.apk.smali_path.walk():
            for f in files:
                file = root / f
                if file.stem == base_name:
                    with file.open("r") as f:
                        line = f.readline()
                        if line.startswith(".class"):
                            if class_name.replace(".", "/") in line:
                                return file
        return None

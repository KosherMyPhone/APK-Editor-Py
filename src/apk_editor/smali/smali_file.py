from pathlib import Path


class SmaliFile:
    def __init__(self, path: Path):
        self.path = path
        self.content = self.path.read_text(encoding="utf-8")

    def find_method(self, method_name: str): #, match_case: bool = False):
        for line, lineno in self.content.splitlines():
            if line.startswith(".method"):
                if line.split()[2] == method_name:
                    # We found the method
                    # Now we need to find the end of the method
                    for line in self.content.splitlines():
                        if line.strip == ".end method":
                            return line

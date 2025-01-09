from pathlib import Path


class SmaliMethod:
    def __init__(self, path: Path, start_line: int):
        self.path = path
        self.file_content = path.read_text(encoding="utf-8")
        self.start_line: int = start_line

    @property
    def end_line(self) -> int:
        with self.path.open("r") as f:
            f.seek(self.start_line)
            for line in f:
                if line.strip() == ".end method":
                    return f.tell()
        raise ValueError("Method does not have an end")

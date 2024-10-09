from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImageTag:
    tag: str
    file: Path

    def to_confluence(self) -> str:
        return f'<ac:image><ri:attachment ri:filename="{self.file.name}" /></ac:image>\n'

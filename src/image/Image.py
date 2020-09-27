from dataclasses import dataclass


@dataclass
class Image:
    name: str
    path: str

    def __init__(self, name: str = "", path: str = "") -> None:
        self.name = name
        self.path = path

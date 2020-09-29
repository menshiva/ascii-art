from dataclasses import dataclass


@dataclass
class Image:
    name: str
    path: str
    contrast: bool
    negative: bool
    convolution: bool

    def __init__(self, name: str, path: str, contrast: bool, negative: bool, convolution: bool) -> None:
        self.name = name
        self.path = path
        self.contrast = contrast
        self.negative = negative
        self.convolution = convolution

    def apply_changes(self, name: str, contrast: bool, negative: bool, convolution: bool):
        # TODO
        self.name = name
        self.contrast = contrast
        self.negative = negative
        self.convolution = convolution

from __future__ import annotations
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

    def apply_changes(self, new_img: Image):
        # TODO
        self.name = new_img.name
        self.contrast = new_img.contrast
        self.negative = new_img.negative
        self.convolution = new_img.convolution

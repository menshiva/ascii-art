from __future__ import annotations
from typing import Tuple, Callable, Any
from dataclasses import dataclass, field

import numpy as np
from imageio import imread

from src.util import Consts


def normalize_uint8(func: Callable[[Image, Any], np.ndarray]) -> np.ndarray:
    def wrapper(self, *args) -> np.ndarray:
        data = func(self, *args)
        data[data < 0] = 0
        data[data > 255] = 255
        return data.astype(np.uint8)

    return wrapper


def format_output_ascii(func: Callable[[Image, Any], np.ndarray]) -> str:
    def wrapper(self, *args) -> str:
        data = func(self, *args)
        return '\n'.join(''.join('%c' % symb for symb in row) for row in data)

    return wrapper


@dataclass
class Image:
    name: str
    path: str
    is_contrast: bool
    is_negative: bool
    is_convolution: bool
    grayscale_level: str
    __width: int = field(init=False)
    __height: int = field(init=False)
    __color_space: int = field(init=False)
    __img_data: np.ndarray = field(init=False)
    __ascii_data: np.chararray = field(init=False)
    __cached_ascii_data: np.chararray = field(init=False)

    def __post_init__(self) -> None:
        if not self.path:
            return
        self.__img_data = np.asarray(imread(self.path))
        img_info: Tuple = self.__img_data.shape
        if len(img_info) == 3:
            self.__height, self.__width, self.__color_space = img_info
            if self.__color_space > 3:
                self.__img_data = self.__img_data[:, :, :3]
                self.__color_space = 3
        else:
            self.__height, self.__width = img_info
            self.__color_space = 1

    def convert_to_ascii_art(self) -> None:
        self.grayscale_level = Consts.uiConsts[
            "DefaultGrayscaleLevel"
        ] if not self.grayscale_level else self.grayscale_level.strip()
        gray_data: np.ndarray = self.__img_data.copy()
        if self.is_convolution:
            gray_data = self.__convolution(gray_data, self.__color_space)
        if self.is_negative:
            gray_data = self.__negative(gray_data)
        if self.is_contrast:
            gray_data = self.__contrast(gray_data)
        if self.__color_space > 1:
            gray_data = self.__rgb_to_gray(gray_data)
        self.__ascii_data = self.__get_ascii_data(gray_data, self.__width, self.__height)
        self.__cached_ascii_data = self.__ascii_data.copy()

    @format_output_ascii
    def get_ascii_art(self, win_width: int, win_height: int) -> np.ndarray:
        (ascii_w, ascii_h) = self.__compute_art_size(win_width, win_height)
        if self.__cached_ascii_data.shape != (ascii_h, ascii_w):
            self.__cached_ascii_data = np.array(
                [[self.__ascii_data[int(self.__height * y / ascii_h)][int(self.__width * x / ascii_w)]
                  for x in range(ascii_w)] for y in range(ascii_h)]
            ).view(np.chararray)
        return self.__cached_ascii_data

    @format_output_ascii
    def export_art(self) -> np.ndarray:
        return self.__ascii_data

    def __get_ascii_data(self, data: np.ndarray, width: int, height: int) -> np.chararray:
        img_data = data.reshape((height, width))
        img_data = (img_data / 255.0 * (len(self.grayscale_level) - 1)).astype(np.int)
        vectorized_grayscale_mask = np.vectorize(self.__grayscale_mask)
        return vectorized_grayscale_mask(img_data, self.grayscale_level)

    def __compute_art_size(self, win_width: int, win_height: int) -> (int, int):
        ascii_h: int
        ascii_w: int
        if win_height >= win_width:
            ascii_w = int(self.__width * (win_height / (self.__height / 2.0)))
            if win_width < ascii_w:
                ascii_h = int(win_height * (float(win_width) / ascii_w))
                ascii_w = win_width
            else:
                ascii_h = win_height
        else:
            ascii_h = int((self.__height / 2.0) * (win_width / self.__width))
            if win_height < ascii_h:
                ascii_w = int(win_width * (float(win_height) / ascii_h))
                ascii_h = win_height
            else:
                ascii_w = win_width
        return int(ascii_w), int(ascii_h)

    @normalize_uint8
    def __compute_kernel(self, kernel: np.ndarray, data: np.ndarray, color_space: int) -> np.ndarray:
        kernelized_colls = []
        for y in range(color_space):
            rolled_rows: np.ndarray = np.roll(data.astype(np.int8), y - 1, axis=0)
            for x in range(color_space):
                rolled_colls: np.ndarray = np.roll(rolled_rows, x - 1, axis=1)
                kernelized_colls.append(rolled_colls * kernel[y, x])
        kernelized_data = np.sum(kernelized_colls, axis=0)
        return kernelized_data

    def __convolution(self, data: np.ndarray, color_space: int) -> np.ndarray:
        convolution_kernel: np.ndarray = np.array(Consts.imageConsts["ConvolutionKernel"])
        return self.__compute_kernel(convolution_kernel, data, color_space)

    @normalize_uint8
    def __contrast(self, data: np.ndarray, contrast_level: float = 255.0) -> np.ndarray:
        factor: float = (259.0 * (contrast_level + 255.0)) / (255.0 * (259.0 - contrast_level))
        non_trunc_contrasted: np.ndarray = (data.astype(np.float) - 128) * factor + 128
        return non_trunc_contrasted

    @staticmethod
    def __negative(data: np.ndarray) -> np.ndarray:
        return 255 - data

    @staticmethod
    def __rgb_to_gray(data: np.ndarray) -> np.ndarray:
        gamma_compressed: np.ndarray = data / 255.0
        linear: np.ndarray = np.where(
            gamma_compressed <= 0.04045,
            gamma_compressed / 12.92,
            ((gamma_compressed + 0.055) / 1.055) ** 2.4
        )
        linear_luminance: np.ndarray = linear @ np.array(Consts.imageConsts["LuminanceCoefficients"]).T
        return (linear_luminance * 255).astype(np.uint8)

    @staticmethod
    def __grayscale_mask(index: int, grayscale_level: str) -> str:
        return grayscale_level[index]

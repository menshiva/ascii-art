from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, Callable, Any

import numpy as np
from numpy import fft
from imageio import imread

from src.util import consts


def normalize_uint8(func: Callable[[Any], np.ndarray]) -> np.ndarray:
    def wrapper(*args) -> np.ndarray:
        data = func(*args)
        data[data < 0] = 0
        data[data > 255] = 255
        return data.astype(np.uint8)

    # noinspection PyTypeChecker
    return wrapper


def format_output_ascii(func: Callable[[Image, Any], np.ndarray]) -> str:
    def wrapper(self, *args) -> str:
        data = func(self, *args)
        return '\n'.join(''.join('%c' % symb for symb in row) for row in data)

    # noinspection PyTypeChecker
    return wrapper


@dataclass
class Image:
    name: str
    path: str
    is_contrast: bool
    is_negative: bool
    is_convolution: bool
    is_emboss: bool
    grayscale_level: str
    __width: int = field(init=False)
    __height: int = field(init=False)
    __color_space: int = field(init=False)
    __image_data_raw: np.ndarray = field(init=False)
    __image_data: np.ndarray = field(init=False)
    __ascii_data: np.chararray = field(init=False)
    __cached_ascii_data: np.chararray = field(init=False)

    @format_output_ascii
    def __str__(self) -> np.ndarray:
        return self.__ascii_data

    def __post_init__(self) -> None:
        if not self.path:
            return
        self.__image_data_raw = np.asarray(imread(self.path))
        img_info = self.__image_data_raw.shape
        if len(img_info) == 3:
            self.__height, self.__width, self.__color_space = img_info
            if self.__color_space > 3:
                self.__image_data_raw = self.__image_data_raw[:, :, :3]
                self.__color_space = 3
        else:
            self.__height, self.__width = img_info
            self.__color_space = 1

    def convert_to_ascii_art(self) -> None:
        self.grayscale_level = self.grayscale_level.strip()
        if not self.grayscale_level:
            self.grayscale_level = consts.uiConsts["DefaultGrayscaleLevel"]
        self.__image_data = self.__image_data_raw.copy()
        if self.is_negative:
            self.__image_data = self.__negative(self.__image_data)
        if self.is_contrast:
            self.__image_data = self.__contrast(self.__image_data)
        if self.__color_space > 1:
            self.__image_data = self.__rgb_to_gray(self.__image_data)
        if self.is_convolution:
            self.__image_data = self.__convolution(self.__image_data)
        if self.is_emboss:
            self.__image_data = self.__emboss(self.__image_data)
        self.__ascii_data = self.__get_ascii_data(
            self.__image_data,
            self.__width, self.__height
        )
        self.__cached_ascii_data = self.__ascii_data.copy()

    @format_output_ascii
    def get_ascii_art(self, win_width: int, win_height: int) -> np.ndarray:
        (ascii_w, ascii_h) = self.__compute_art_size(win_width, win_height)
        if self.__cached_ascii_data.shape != (ascii_h, ascii_w):
            self.__cached_ascii_data = np.array([
                [self.__ascii_data[
                     int(self.__height * y / ascii_h)
                 ][
                     int(self.__width * x / ascii_w)
                 ] for x in range(ascii_w)
                 ] for y in range(ascii_h)
            ]).view(np.chararray)
        return self.__cached_ascii_data

    def get_image_data(self) -> np.ndarray:
        return self.__image_data

    def __get_ascii_data(self, data: np.ndarray,
                         width: int, height: int) -> np.chararray:
        grayscale_indices = (
                data.reshape((height, width))
                / 255.0
                * (len(self.grayscale_level) - 1)
        ).astype(np.uint8)
        apply_mask_vectorized = np.vectorize(self.__apply_grayscale_mask)
        return apply_mask_vectorized(grayscale_indices, self.grayscale_level)

    def __compute_art_size(self,
                           win_width: int, win_height: int) -> Tuple[int, int]:
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
        return ascii_w, ascii_h

    @staticmethod
    def __negative(data: np.ndarray) -> np.ndarray:
        return 255 - data

    @staticmethod
    @normalize_uint8
    def __contrast(data: np.ndarray) -> np.ndarray:
        contrast_level = 255.0
        factor = ((259.0 * (contrast_level + 255.0))
                  / (255.0 * (259.0 - contrast_level)))
        non_trunc_contrasted = (data.astype(np.float) - 128) * factor + 128
        return non_trunc_contrasted

    def __convolution(self, data: np.ndarray) -> np.ndarray:
        convolution_kernel = np.array(consts.imageConsts["ConvolutionKernel"])
        return self.__compute_kernel(data, convolution_kernel)

    def __emboss(self, data: np.ndarray) -> np.ndarray:
        emboss_kernel = np.array(consts.imageConsts["EmbossKernel"])
        return self.__compute_kernel(data, emboss_kernel)

    @staticmethod
    @normalize_uint8
    def __compute_kernel(data: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        new_h = (data.shape[0] - kernel.shape[0]) // 2
        new_w = (data.shape[1] - kernel.shape[1]) // 2
        kernel = np.pad(kernel, (
            (new_h, new_h + int(data.shape[0] % 2 == 0)),
            (new_w, new_w + int(data.shape[1] % 2 == 0))
        ))

        data_transformed = fft.fft2(data)
        kernel_flipped_transormed = fft.fft2(np.flipud(np.fliplr(kernel)))
        h, w = data_transformed.shape
        kernelized = np.real(
            fft.ifft2(data_transformed * kernel_flipped_transormed)
        )
        kernelized = np.roll(kernelized, -h // 2 + 1, axis=0)
        kernelized = np.roll(kernelized, -w // 2 + 1, axis=1)
        return kernelized

    @staticmethod
    def __rgb_to_gray(data: np.ndarray) -> np.ndarray:
        gamma_compressed = data / 255.0
        linear = np.where(
            gamma_compressed <= 0.04045,
            gamma_compressed / 12.92,
            ((gamma_compressed + 0.055) / 1.055) ** 2.4
        )
        linear_luminance = linear @ np.array(
            consts.imageConsts["LuminanceCoefficients"]
        ).T
        return (linear_luminance * 255).astype(np.uint8)

    @staticmethod
    def __apply_grayscale_mask(index: int, grayscale_level: str) -> str:
        return grayscale_level[index]

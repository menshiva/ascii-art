from __future__ import annotations
from typing import Tuple
from imageio import imread
from src.image.util.ImageConsts import imageConsts
import numpy as np


class Image:
    name: str
    path: str
    is_contrast: bool
    is_negative: bool
    is_convolution: bool
    __width: int
    __height: int
    __color_space: int
    __img_data: np.ndarray
    __ascii_data: np.chararray
    __cached_ascii_data: np.chararray
    __grayscale_level: str

    def __init__(self, name: str, path: str, glvl: str, contrast: bool, negative: bool, convolution: bool) -> None:
        self.name = name
        self.path = path
        self.is_contrast = contrast
        self.is_negative = negative
        self.is_convolution = convolution
        if not glvl:
            self.__grayscale_level = imageConsts["DefaultGrayscaleLevel"]
        else:
            self.__grayscale_level = glvl

        self.__img_data = np.asarray(imread(path))
        img_info: Tuple = self.__img_data.shape
        if len(img_info) == 3:
            self.__height, self.__width, self.__color_space = img_info
            if self.__color_space > 3:
                self.__img_data = self.__img_data[:, :, :3]
        else:
            self.__height, self.__width = img_info
            self.__color_space = 1

        self.__convert_to_ascii_art(self.is_contrast, self.is_negative, self.is_convolution)

    def apply_changes(self, new_img: Tuple[str, str, bool, bool, bool]) -> None:
        self.name, glvl, self.is_contrast, self.is_negative, self.is_convolution = new_img
        if not glvl:
            self.__grayscale_level = imageConsts["DefaultGrayscaleLevel"]
        else:
            self.__grayscale_level = glvl
        self.__convert_to_ascii_art(self.is_contrast, self.is_negative, self.is_convolution)

    def get_ascii_art(self, win_width: int, win_height: int) -> str:
        (ascii_w, ascii_h) = self.__compute_art_size(win_width, win_height)
        if self.__cached_ascii_data.shape != (ascii_h, ascii_w):
            self.__cached_ascii_data = np.array(
                [[self.__ascii_data[int(self.__height * y / ascii_h)][int(self.__width * x / ascii_w)]
                  for x in range(ascii_w)] for y in range(ascii_h)]
            ).view(np.chararray)
        return '\n'.join(''.join('%c' % symb for symb in row) for row in self.__cached_ascii_data)

    def __convert_to_ascii_art(self, contrast: bool, negative: bool, convolution: bool) -> None:
        gray_data: np.ndarray = self.__img_data.copy()
        if convolution:
            gray_data = self.__convolution(gray_data, self.__color_space)
        if negative:
            gray_data = self.__negative(gray_data)
        if contrast:
            gray_data = self.__contrast(gray_data)
        if self.__color_space > 1:
            gray_data = self.__grayscale(gray_data)
        self.__ascii_data = self.__get_ascii_data(gray_data, self.__width, self.__height)
        self.__cached_ascii_data = self.__ascii_data.copy()

    def __compute_kernel(self, kernel: np.ndarray, data: np.ndarray, color_space: int) -> np.ndarray:
        kernelized_colls = []
        for y in range(color_space):
            rolled_rows: np.ndarray = np.roll(data.astype(np.int8), y - 1, axis=0)
            for x in range(color_space):
                rolled_colls: np.ndarray = np.roll(rolled_rows, x - 1, axis=1)
                kernelized_colls.append(rolled_colls * kernel[y, x])
        kernelized_data: np.ndarray = self.__normalize_uint8(np.sum(kernelized_colls, axis=0))
        return kernelized_data

    def __convolution(self, data: np.ndarray, color_space: int) -> np.ndarray:
        convolution_kernel: np.ndarray = np.array(imageConsts["ConvolutionKernel"])
        return self.__compute_kernel(convolution_kernel, data, color_space)

    @staticmethod
    def __negative(data: np.ndarray) -> np.ndarray:
        return 255 - data

    def __contrast(self, data: np.ndarray, contrast_level: float = 255.0) -> np.ndarray:
        factor: float = (259.0 * (contrast_level + 255.0)) / (255.0 * (259.0 - contrast_level))
        non_trunc_contrasted: np.ndarray = (data.astype(np.float) - 128) * factor + 128
        return self.__normalize_uint8(non_trunc_contrasted)

    @staticmethod
    def __grayscale(data: np.ndarray) -> np.ndarray:
        gamma_compressed: np.ndarray = data / 255.0
        linear: np.ndarray = np.where(
            gamma_compressed <= 0.04045,
            gamma_compressed / 12.92,
            ((gamma_compressed + 0.055) / 1.055) ** 2.4
        )
        linear_luminance: np.ndarray = linear @ np.array(imageConsts["LuminanceCoefficients"]).T
        return (linear_luminance * 255).astype(np.uint8)

    def __get_ascii_data(self, data: np.ndarray, width: int, height: int) -> np.chararray:
        img_data = data.reshape((height, width))
        img_data = (img_data / 255.0 * (len(self.__grayscale_level) - 1)).astype(np.int)
        vectorized_grayscale_mask = np.vectorize(self.__grayscale_mask)
        return vectorized_grayscale_mask(img_data, self.__grayscale_level)

    @staticmethod
    def __grayscale_mask(index: int, grayscale_level: str) -> str:
        return grayscale_level[index]

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

    @staticmethod
    def __normalize_uint8(data: np.ndarray) -> np.ndarray:
        data[data < 0] = 0
        data[data > 255] = 255
        return data.astype(np.uint8)

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, Callable, Any

import numpy as np
from numpy import fft
from imageio import imread

from src.util import consts


def normalize_uint8(func: Callable[[Any], np.ndarray]) -> np.ndarray:
    """
    Decorator for image data normalization.

    Accepts NumPy array from func and safely (without overflow)
    truncates it's values so they fits in uint8 type.

    Args:
        func: Callable[[Any], np.ndarray]
            Function returning NumPy array.

    Returns:
        Truncated NumPy array.
    """

    def wrapper(*args) -> np.ndarray:
        data = func(*args)
        data[data < 0] = 0
        data[data > 255] = 255
        return data.astype(np.uint8)

    # noinspection PyTypeChecker
    return wrapper


def format_output_ascii(func: Callable[[Any], np.chararray]) -> str:
    """
    Decorator for formatting ASCII art output.

    Accepts NumPy char array from func and converts it into string.

    Args:
        func: Callable[[Any], np.chararray]
            Function returning NumPy char array.

    Returns:
        Formatted string.
    """

    def wrapper(*args) -> str:
        data = func(*args)
        return '\n'.join(''.join('%c' % symb for symb in row) for row in data)

    # noinspection PyTypeChecker
    return wrapper


@dataclass
class Image:
    """
    Data class for all supported image formats.

    This class holds all data, needed for raw format without any compression.
    Operates with image in common way, such as:
    read from path, convert to ASCII, add effect etc.

    Attributes:
        name: str
            Image's given name.
        path: str
            Path to image file.
        is_contrast: bool
            Flag, which indicates if contrast effect is applied.
        is_negative: bool
            Flag, which indicates if negative effect is applied.
        is_sharpen: bool
            Flag, which indicates if sharpen effect is applied.
        is_emboss: bool
            Flag, which indicates if emboss effect is applied.
        grayscale_level: str
            Range of symbols from darkest to lightest,
            whiches used for ASCII convertation.
        __width: int
            Width of image (in pixels count).
        __height: int
            Height of image (in pixels count).
        __color_space: int
            Image's channels count.
        __image_data_raw: np.ndarray
            List of color components values, which were read from image file.
        __image_data: np.ndarray
            Copy of __image_data_raw, which has effects
            applied and converted to grayscale.
        __ascii_data: np.chararray
            Copy of __image_data converted to ASCII art.
        __cached_ascii_data: np.chararray
            Copy of __ascii_data scaled to the window size.
    """

    name: str
    path: str
    is_contrast: bool
    is_negative: bool
    is_sharpen: bool
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
    def __str__(self) -> np.chararray:
        """
        x.__str__() <==> str(x)

        Returns:
            ASCII art in full image size.
        """

        return self.__ascii_data

    def __post_init__(self) -> None:
        """
        Reads image from path.

        Gets it's width, height and color space.
        Optionally truncates it's aplha channel.

        Returns:
            None.
        """

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
        """
        General function for ASCII art conversion.

        Updates grayscale_level, applies all effects on image
        and converts it from RGB to grayscale.

        Returns:
            None.
        """

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
        if self.is_sharpen:
            self.__image_data = self.__sharpen(self.__image_data)
        if self.is_emboss:
            self.__image_data = self.__emboss(self.__image_data)
        self.__ascii_data = self.__get_ascii_data()
        self.__cached_ascii_data = self.__ascii_data.copy()

    @format_output_ascii
    def get_ascii_art(self, win_width: int, win_height: int) -> np.chararray:
        """
        If win_width and win_height aren't equal to __cached_ascii_data -
        computes ASCII art with size, based on window's and image's sizes, and
        saves it in __cached_ascii_data (performance improvement).

        Args:
            win_width: int
                Width of window, in which art will be drawn.
            win_height: int
                Height of window, in which art will be drawn.

        Returns:
            __cached_ascii_data.
        """

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
        """
        Returns:
            __image_data.
        """

        return self.__image_data

    def __get_ascii_data(self) -> np.chararray:
        """
        Converts image data to ASCII art.

        Finds needful ASCII character in grayscale level
        by brightness level of image data's values.
        Uses NumPy vectorization (performance improvement).

        Returns:
            NumPy char array of __image_data converted to ASCII art.
        """

        grayscale_indices = (
                self.__image_data.reshape((self.__height, self.__width))
                / 255.0
                * (len(self.grayscale_level) - 1)
        ).astype(np.uint8)
        apply_mask_vectorized = np.vectorize(self.__apply_grayscale_mask)
        return apply_mask_vectorized(grayscale_indices, self.grayscale_level)

    def __compute_art_size(self,
                           win_width: int,
                           win_height: int) -> Tuple[int, int]:
        """
        Computes new width and height for ASCII art to fit in,
        based on width and height of window and image.

        Computations preserves image's aspect ratio.

        Args:
            win_width: int
                Width of window, in which art will be drawn.
            win_height: int
                Height of window, in which art will be drawn.

        Returns:
            Pair of ASCII art's width and height.
        """

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
        """
        Applies negative effect.

        Args:
            data: np.ndarray
                Image data.

        Returns:
            Image data with negative effect.
        """

        return 255 - data

    @staticmethod
    @normalize_uint8
    def __contrast(data: np.ndarray) -> np.ndarray:
        """
        Applies contrast effect.

        Args:
            data: np.ndarray
                Image data.

        Returns:
            Image data with contrast effect.
        """

        contrast_level = 255.0
        factor = ((259.0 * (contrast_level + 255.0))
                  / (255.0 * (259.0 - contrast_level)))
        non_trunc_contrasted = (data.astype(np.float) - 128) * factor + 128
        return non_trunc_contrasted

    def __sharpen(self, data: np.ndarray) -> np.ndarray:
        """
        Applies sharpen effect.

        Args:
            data: np.ndarray
                Image data.

        Returns:
            Image data with sharpen effect.
        """

        sharpen_kernel = np.array(consts.imageConsts["SharpenKernel"])
        return self.__compute_kernel(data, sharpen_kernel)

    def __emboss(self, data: np.ndarray) -> np.ndarray:
        """
        Applies emboss effect.

        Args:
            data: np.ndarray
                Image data.

        Returns:
            Image data with emboss effect.
        """

        emboss_kernel = np.array(consts.imageConsts["EmbossKernel"])
        return self.__compute_kernel(data, emboss_kernel)

    @staticmethod
    @normalize_uint8
    def __compute_kernel(data: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        """
        Helper function for computing sharpen (image kernel).

        Computes image kernel using discrete Fourier Transform
        and applies sharpen kernel-based (sharpen, emboss etc.) effects.

        Args:
            data: np.ndarray
                Image data.
            kernel: np.ndarray
                3x3 effect kernel.

        Returns:
            Kernelized image data with applied kernel-based effect.
        """

        new_kernel_size = (
            data.shape[0] - kernel.shape[0],
            data.shape[1] - kernel.shape[1]
        )
        kernel_padding = (
            ((new_kernel_size[0] + 1) // 2, new_kernel_size[0] // 2),
            ((new_kernel_size[1] + 1) // 2, new_kernel_size[1] // 2)
        )
        padded_kernel = np.pad(kernel, kernel_padding)
        # move FFT origin to the middle
        shifted_kernel = fft.ifftshift(padded_kernel)

        kernelized = np.real(
            fft.ifft2(fft.fft2(data) * fft.fft2(shifted_kernel))
        )
        return kernelized

    @staticmethod
    def __rgb_to_gray(data: np.ndarray) -> np.ndarray:
        """
        Converts RGB image to grayscale image.

        Function uses perceptual luminance-preserving conversion algorithm
        so grayscale image would preserve brightness measure
        (much better for ASCII representation).

        Args:
            data: np.ndarray
                Image data.

        Returns:
            Grayscale image data with 1 gray channel.
        """

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
        """
        Helper function for mapping grayscale level symbol
        to image data values' brightness.

        Should be used with NumPy vectorization (performance improvement).

        Args:
            index: int
                Relation between brightness of image data and grayscale level.
            grayscale_level: str
                Grayscale level defining symbols from darkest to lightest.

        Returns:
            Image's gray pixel represented as ASCII symbol.
        """

        return grayscale_level[index]

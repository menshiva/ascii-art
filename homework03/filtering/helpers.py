import numpy as np
from PIL import Image
from IPython.display import display

identity_kernel = np.array([
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0],
])

sharpening_kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0],
])

approx_gaussian_blur_3_kernel = (1 / 16) * np.array([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1],
])

approx_gaussian_blur_5_kernel = (1 / 256) * np.array([
    [1, 4, 6, 4, 1],
    [4, 16, 24, 16, 4],
    [6, 24, 36, 24, 6],
    [4, 16, 24, 16, 4],
    [1, 4, 6, 4, 1],
])

edge_detection_kernel = np.array([
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1],
])

embossing_kernel = np.array([
    [-2, -1, 0],
    [-1, 1, 1],
    [0, 1, 2]
])

# for interested people https://en.wikipedia.org/wiki/Roberts_cross
roberts_cross_1_kernel = np.array([
    [1, 0],
    [0, -1],
])

roberts_cross_2_kernel = np.array([
    [0, 1],
    [-1, 0],
])

filters = {
    'Identity': identity_kernel,
    'Sharpening': sharpening_kernel,
    'Gaussian blur 3x3 (approx)': approx_gaussian_blur_3_kernel,
    'Gaussian blur 5x5 (approx)': approx_gaussian_blur_5_kernel,
    'Edge detection': edge_detection_kernel,
    'Embossing': embossing_kernel,
}


def read_image(file_name: str) -> np.array:
    return np.asarray(Image.open(file_name), dtype=np.uint8)


def image_from_array(array, mode):
    return Image.fromarray(array, mode=mode)


def display_image(array, mode='RGB'):
    display(image_from_array(array, mode=mode))


def save_image(array, file_path, mode='RGB'):
    image_from_array(array, mode=mode).save(file_path)

from typing import Tuple
import numpy as np


def create_padded_template(image: np.array, kernel: np.array) -> (np.array, Tuple[int, int]):
    if kernel.shape[0] % 2 == 0:
        kernel_pad = kernel.shape
    else:
        kernel_pad = (kernel.shape[0] - 1, kernel.shape[1] - 1)
    image_padded = np.zeros((
        image.shape[0] + kernel_pad[0],
        image.shape[1] + kernel_pad[1]
    ))
    return image_padded, (kernel_pad[0] // 2, kernel_pad[1] // 2)


def apply_kernel(image: np.array, kernel: np.array, template: np.array, frm: Tuple[int, int]) -> np.array:
    template[frm[0]:-frm[0], frm[1]:-frm[1]] = image
    output = np.zeros_like(image, np.float)

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            part = template[y: y + kernel.shape[0], x: x + kernel.shape[1]]
            output[y, x] = np.sum(part * kernel)

    return np.clip(output, 0.0, 255.0).astype(np.uint8)


def apply_filter(image: np.array, kernel: np.array) -> np.array:
    assert image.ndim in [2, 3]
    assert kernel.ndim == 2
    assert kernel.shape[0] == kernel.shape[1]

    if image.ndim == 2:
        padded_template, frm = create_padded_template(image, kernel)
        result = apply_kernel(image, kernel, padded_template, frm)
    else:
        padded_template, frm = create_padded_template(image[:, :, 0], kernel)
        result = np.zeros_like(image, np.uint8)
        result[:, :, 0] = apply_kernel(image[:, :, 0], kernel, padded_template, frm)
        result[:, :, 1] = apply_kernel(image[:, :, 1], kernel, padded_template, frm)
        result[:, :, 2] = apply_kernel(image[:, :, 2], kernel, padded_template, frm)
    return result

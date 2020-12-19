import os
import sys

from numpy.testing import assert_equal
import numpy as np
from imageio import imread, imwrite

from src.image import Image
from src.util import consts


def relative_path(rp: str) -> str:
    return os.path.join(sys.path[0], rp)


def test_contrast_effect():
    img = Image(
        "", relative_path("tests/data/lenna.png"),
        True, False, False, False,
        consts.uiConsts["DefaultGrayscaleLevel"]
    )
    img.convert_to_ascii_art()
    assert_equal(
        img.get_image_data(),
        np.asarray(imread(relative_path("tests/data/lenna_contrast.ppm")))
    )


def test_negative_effect():
    img = Image(
        "", relative_path("tests/data/lenna.png"),
        False, True, False, False,
        consts.uiConsts["DefaultGrayscaleLevel"]
    )
    img.convert_to_ascii_art()
    assert_equal(
        img.get_image_data(),
        np.asarray(imread(relative_path("tests/data/lenna_negative.ppm")))
    )


def test_sharpen_effect():
    img = Image(
        "", relative_path("tests/data/lenna.png"),
        False, False, True, False,
        consts.uiConsts["DefaultGrayscaleLevel"]
    )
    img.convert_to_ascii_art()
    assert_equal(
        img.get_image_data(),
        np.asarray(imread(relative_path("tests/data/lenna_sharpen.ppm")))
    )


def test_emboss_effect():
    img = Image(
        "", relative_path("tests/data/lenna.png"),
        False, False, False, True,
        consts.uiConsts["DefaultGrayscaleLevel"]
    )
    img.convert_to_ascii_art()
    assert_equal(
        img.get_image_data(),
        np.asarray(imread(relative_path("tests/data/lenna_emboss.ppm")))
    )


def test_gray_effect():
    img = Image(
        "", relative_path("tests/data/lenna.png"),
        False, False, False, False,
        consts.uiConsts["DefaultGrayscaleLevel"]
    )
    img.convert_to_ascii_art()
    assert_equal(
        img.get_image_data(),
        np.asarray(imread(relative_path("tests/data/lenna_gray.ppm")))
    )


def test_ascii_art_full():
    img = Image(
        "", relative_path("tests/data/lenna.png"),
        True, False, False, False,
        consts.uiConsts["DefaultGrayscaleLevel"]
    )
    img.convert_to_ascii_art()
    with open(relative_path("tests/data/lenna_ascii_full.txt")) as f:
        assert_equal(str(img), f.read())


def test_ascii_art_resize():
    img = Image(
        "", relative_path("tests/data/lenna.png"),
        True, False, False, False,
        consts.uiConsts["DefaultGrayscaleLevel"]
    )
    img.convert_to_ascii_art()
    with open(relative_path("tests/data/lenna_ascii_378x189.txt")) as f:
        assert_equal(str(img.get_ascii_art(378, 189)), f.read())


def test_all():
    img = Image(
        "", relative_path("tests/data/lenna.png"),
        True, True, True, True,
        "@o."
    )
    img.convert_to_ascii_art()
    with open(relative_path("tests/data/lenna_ascii_all.txt")) as f:
        assert_equal(str(img), f.read())

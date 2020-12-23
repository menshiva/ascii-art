import os
import sys

import numpy as np
import pytest
from imageio import imread
from numpy.testing import assert_equal

from src.util import consts


def relative_path(rp: str) -> str:
    return os.path.join(sys.path[0], rp)


@pytest.fixture
def lenna():
    from src.image import Image
    return Image(
        "Lenna", relative_path("tests/data/lenna.png"),
        False, False, False, False,
        consts.uiConsts["DefaultGrayscaleLevel"]
    )


def test_info(lenna):
    assert lenna.name == "Lenna"
    assert lenna.get_width() == lenna.get_height() == 512
    assert lenna.get_color_space() == 3


@pytest.mark.parametrize("effect", ("gray", "contrast", "negative", "sharpen", "emboss"))
def test_effects(lenna, effect: str):
    if effect == "gray":
        lenna.set_effect_flags(False, False, False, False)
    elif effect == "contrast":
        lenna.set_effect_flags(True, False, False, False)
    elif effect == "negative":
        lenna.set_effect_flags(False, True, False, False)
    elif effect == "sharpen":
        lenna.set_effect_flags(False, False, True, False)
    else:
        lenna.set_effect_flags(False, False, False, True)
    lenna.convert_to_ascii_art()
    assert_equal(
        lenna.get_image_data(),
        np.asarray(imread(relative_path(f"tests/data/lenna_{effect}.ppm")))
    )


def test_ascii_art_full(lenna):
    lenna.set_effect_flags(True, False, False, False)
    lenna.convert_to_ascii_art()
    with open(relative_path("tests/data/lenna_ascii_full.txt")) as f:
        assert_equal(str(lenna), f.read())


def test_ascii_art_resize(lenna):
    lenna.set_effect_flags(True, False, False, False)
    lenna.convert_to_ascii_art()
    with open(relative_path("tests/data/lenna_ascii_378x189.txt")) as f:
        assert_equal(str(lenna.get_ascii_art(378, 189)), f.read())


def test_all(lenna):
    lenna.set_effect_flags(True, True, True, True)
    lenna.grayscale_level = "@o."
    lenna.convert_to_ascii_art()
    with open(relative_path("tests/data/lenna_ascii_all.txt")) as f:
        assert_equal(str(lenna), f.read())

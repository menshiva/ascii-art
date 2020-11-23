from pytest import fixture
from numpy.testing import assert_equal

from filtering.helpers import *
#from filtering.filtering_sln import apply_filter
from filtering.filtering import apply_filter


@fixture
def image():
    return read_image('tests/lenna.png')


@fixture
def image_gaussian_blur():
    return read_image('tests/lenna_gaussian_blur.png')


@fixture
def image_gray(image):
    return np.average(image.astype(np.float), weights=[0.299, 0.587, 0.114], axis=2).astype(np.uint8)


@fixture
def image_gray_edge_detection():
    return read_image('tests/lenna_gray_edge_detection.png')


@fixture
def image_roberts_cross():
    return read_image('tests/lenna_roberts_cross.png')


def test_identity_filter(image):
    assert_equal(image, apply_filter(image, identity_kernel))


def test_gaussian_blur(image, image_gaussian_blur):
    assert_equal(apply_filter(image, approx_gaussian_blur_5_kernel), image_gaussian_blur)


def test_gray_edge_detection(image_gray, image_gray_edge_detection):
    assert_equal(apply_filter(image_gray, edge_detection_kernel), image_gray_edge_detection)


def test_roberts_cross_operator(image_gray, image_roberts_cross):
    assert_equal(
        apply_filter(apply_filter(image_gray, roberts_cross_1_kernel), roberts_cross_2_kernel),
        image_roberts_cross)

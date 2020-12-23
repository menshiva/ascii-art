import pytest


@pytest.fixture
def factory():
    from src.factory import ArtFactory
    from src.image import Image
    factory = ArtFactory()
    for i in range(10):
        factory += Image(
            f"Lenna{i}", "",
            False, False, False, False,
            ""
        )
    return factory


def test_adding(factory):
    assert len(factory) == 10
    assert factory[0].name == "Lenna9"
    assert factory[9].name == "Lenna0"
    assert 5 in factory
    assert 9 in factory
    assert 10 not in factory


def test_iterating_over(factory):
    summ = 0
    for img in iter(factory):
        summ += int(img.name[-1])
        if img.name[-1] == '5':
            img.name = "Lenna50"

    assert summ == 45
    assert factory[4].name == "Lenna50"


def test_changes(factory):
    for img in iter(factory):
        img.name = str((int(img.name[-1]) + 1) ** 2)

    assert (int(factory[6].name) + int(factory[7].name)) ** (1/2) == 5

    for i, _ in enumerate(factory):
        if int(factory[i].name) % 2 == 1:
            del factory[i]

    summ = 0
    for img in iter(factory):
        summ += int(img.name)

    assert len(factory) == 5
    assert summ == 220

from src.factory.ArtFactory import ArtFactory
from src.gui.Gui import Gui
from src.image.Image import Image


def add_art(gui: Gui,
            name: str, path: str, grayscale: str,
            contrast: bool, negative: bool, convolution: bool) -> None:
    gui.addImageDialog.setImageLoading(True)
    gui.artFactory.lastDrawedArt += 1
    gui.process_image_background(-1, name, path, grayscale, contrast, negative, convolution)


def edit_art(gui: Gui, index: int,
             name: str, grayscale: str,
             contrast: bool, negative: bool, convolution: bool) -> None:
    gui.addImageDialog.setImageLoading(True)
    old_img = gui.artFactory[index]
    gui.process_image_background(index, name, old_img.path, grayscale, contrast, negative, convolution)


def on_image_processed(gui: Gui, img: Image, index: int) -> None:
    if index == -1:
        gui.artFactory += img
        if len(gui.artFactory) > 1:
            gui.set_play_animation_button_enable(True)
        gui.addImageDialog.clearInput()
    else:
        gui.artFactory[index] = img
        if gui.artFactory.lastDrawedArt == index:
            draw_art(gui, index)
        gui.addImageDialog.close()
    gui.addImageDialog.setImageLoading(False)


def remove_art(gui: Gui, index: int) -> None:
    if index < gui.artFactory.lastDrawedArt:
        gui.artFactory.lastDrawedArt -= 1
    del gui.artFactory[index]
    if len(gui.artFactory) < 2:
        gui.set_play_animation_button_enable(False)


def open_art_dialog(gui: Gui, index: int) -> None:
    if index == -1:
        gui.addImageDialog.openDialog(-1, "", "", True, False, False)
    else:
        image = gui.artFactory[index]
        gui.addImageDialog.openDialog(
            index, image.name, image.path, image.is_contrast, image.is_negative, image.is_convolution
        )


def draw_art(gui: Gui, index: int) -> None:
    if index == -1 or index not in gui.artFactory:
        gui.artFactory.lastDrawedArt = -1
        gui.print_art("")
        return
    gui.artFactory.lastDrawedArt = index
    (char_width, char_height) = gui.compute_art_label_size()
    art: str = gui.artFactory[index].get_ascii_art(char_width, char_height)
    gui.print_art(art)


def apply_grayscale(gui: Gui, grayscale: str) -> None:
    for i, art in enumerate(gui.artFactory):
        edit_art(gui, i, art.name, grayscale, art.is_contrast, art.is_negative, art.is_convolution)


def main():
    art_factory = ArtFactory()
    gui = Gui(art_factory)
    gui.onAddArtCallback = add_art
    gui.onEditArtCallback = edit_art
    gui.onImageProcessed = on_image_processed
    gui.onRemoveArtCallback = remove_art
    gui.onOpenArtDialogCallback = open_art_dialog
    gui.onDrawArtCallback = draw_art
    gui.onApplyGrayscale = apply_grayscale
    gui.exec()


if __name__ == '__main__':
    main()

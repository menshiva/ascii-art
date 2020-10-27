import os
import sys

from imageio import imwrite

from src.factory import ArtFactory
from src.gui import Gui
from src.image import Image


def save_preview(preview: Image) -> str:
    tmp_path: str = os.path.join(sys.path[0], "tmp.ppm")
    imwrite(tmp_path, preview.get_image_data())
    return tmp_path


def on_open_art_dialog(gui: Gui, index: int) -> None:
    if index == -1:
        gui.imageDialog.openDialog(-1, "", "", "", False, False, False, False)
    else:
        image = gui.artFactory[index]
        preview_path = save_preview(image)
        gui.imageDialog.openDialog(
            index, preview_path,
            image.name, image.path,
            image.is_contrast, image.is_negative,
            image.is_convolution, image.is_emboss
        )


def on_preview_art(gui: Gui, image: Image) -> None:
    gui.imageDialog.setImageLoading(True)
    gui.process_image_background(-1, image)


def on_image_processed(gui: Gui, index: int) -> None:
    if index == -1:
        preview_path = save_preview(gui.artFactory.loaded_image)
        gui.imageDialog.setPreview(preview_path)
        gui.imageDialog.setImageLoading(False)
    elif gui.get_current_art_list_index() == index:
        on_draw_art(gui, index)


def on_add_edit_art(gui: Gui, index: int, name: str) -> None:
    new_image = gui.artFactory.loaded_image
    new_image.name = name
    if index == -1:
        gui.artFactory += new_image
        if len(gui.artFactory) > 1:
            gui.set_play_animation_button_enable(True)
    else:
        gui.artFactory[index] = new_image
        if gui.get_current_art_list_index() == index:
            on_draw_art(gui, index)


def on_draw_art(gui: Gui, index: int) -> None:
    if index == -1 or index not in gui.artFactory:
        gui.print_art("")
        return
    (char_width, char_height) = gui.compute_art_label_size()
    # noinspection PyTypeChecker
    art: str = gui.artFactory[index].get_ascii_art(char_width, char_height)
    gui.print_art(art)


def on_remove_art(gui: Gui, index: int) -> None:
    del gui.artFactory[index]
    if len(gui.artFactory) < 2:
        gui.set_play_animation_button_enable(False)


def on_apply_grayscale(gui: Gui, new_grayscale: str) -> None:
    for i, art in enumerate(gui.artFactory):
        art.grayscale_level = new_grayscale
        gui.process_image_background(i, art)


def main():
    art_factory = ArtFactory()
    gui = Gui(art_factory)
    gui.on_open_art_dialog = on_open_art_dialog
    gui.on_preview_art = on_preview_art
    gui.on_image_processed = on_image_processed
    gui.on_add_edit_art = on_add_edit_art
    gui.on_draw_art = on_draw_art
    gui.on_remove_art = on_remove_art
    gui.on_apply_grayscale = on_apply_grayscale
    gui.exec()


if __name__ == '__main__':
    main()

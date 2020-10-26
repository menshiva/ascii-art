<dl>
    <h1 align="center">
        <img src="./img/logo.png" alt="ASCII Art" width="192">
        <br><br>ASCII Art<br>
    </h1>
    <h4 align="center">A minimal image to ASCII art convertation desktop app.</h4>
    <p align="center">
        <a href="#key-features-">Key Features 🍪</a> |
        <a href="#dependencies-">Dependencies 🧬</a> |
        <a href="#build-">Build 🚀</a> |
        <a href="#credits-">Credits ✍</a>
    </p>
    <h1 align="center">
        <img src="https://raw.githubusercontent.com/amitmerchant1990/electron-markdownify/master/app/img/markdownify.gif" alt="Preview">
    </h1>
</dl>

## Key Features 🍪

* Supporting JPEG, PNG, PPM, PGM image formats
* Light / Dark mode
* ASCII art symbols size adjustment
* Your own ASCII art symbol style!
* ASCII art animation with speed adjustment
* Export art to .txt file in full image resolution
* Supporting art effects:
  - _Contrast_
  - _Negative_
  - _Convolution_

## Dependencies 🧬

Minimal requirements:
* Python 3.8.1
* NumPy 1.19.2
* PySide2 5.15.1
* imageio 2.9.0

## Build 🚀

#### Download
Download this project manually with download button or run from your command line:
```bash
$ git clone --single-branch --branch ascii-art https://gitlab.fit.cvut.cz/BI-PYT/b201/menshiva.git
```

#### Change working directory
Change your working directory with command:
```bash
$ cd menshiva
```

#### Install dependencies
Run this command to install all necessary dependencies:
```bash
$ pip install -r requirements.txt
```

#### Run application
Use this command to run ASCII Art:
```bash
$ python3 app.py
```

## Credits ✍

#### Third-party libraries
* [NumPy](https://numpy.org/)
* [Qt for Python](https://wiki.qt.io/Qt_for_Python)
* [imageio](https://imageio.github.io/)

#### Sources of used algorithms
* [Image scailing algorithm](https://en.wikipedia.org/wiki/Image_scaling#Nearest-neighbor_interpolation)
* [RGB to grayscale preserving luminance algorithm](https://en.wikipedia.org/wiki/Grayscale#Colorimetric_(perceptual_luminance-preserving)_conversion_to_grayscale)
* [Contrast effect algorithm](https://en.wikipedia.org/wiki/Contrast_(vision))
* [Convolution effect kernel algorithm](https://setosa.io/ev/image-kernels/)

#### Related
* Special thanks to [Freepik](https://www.flaticon.com/authors/freepik) for app icon!

#### Author
* Ivan Menshikov (menshiva@fit.cvut.cz)
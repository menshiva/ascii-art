# HW3: Image filtering

Your assignment is to implement a method that will take an image and a filter and applies a [convolution](https://en.wikipedia.org/wiki/Kernel_%28image_processing%29) between them. Only 2D filters (of any dimension) will be used and the method has to be able to handle both grayscale and RGB images. In case of RGB images, the filter is applied to each channel independently. When applying the filter, the pixels outside of the image boundary should be filled with zeros. You can assume that the kernels are square.

Only `numpy` and basic operations such as multiplication and sum can be used. So you cannot use `scipy`, for example.
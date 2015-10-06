from PIL import Image
import math
import numpy as np


class SheetImageSlice(object):
# defines general methods for getting data from a sliced image
    def __init__(self, image, x=0, y=0):
        # Constants
        self.THRESHOLDING_TO_BLACK = 43

        # initializes image metadata from analyzing image
        # convert to pure b/w
        # self.image = image.point(lambda x: x > self.THRESHOLDING_TO_BLACK and 255, "1")
        self.image = image.convert("1", dither=None)
        self.image_array = np.asarray(image)
        # x and y determine position relative to base image
        self.x = x
        self.y = y

        self.load_pixels()

    def load_pixels(self):
        self.pixels = self.image.load()

    def slice(self, x, y, width, height):
        # returns a slice of itself as an image
        return self.image.crop((x, y, x+width, y+height))

    # as well as its constituents
    def get_width(self):
        # returns the width of the provided image
        return self.get_dimensions()[0]

    def get_height(self):
        # returns the width of the provided image
        return self.get_dimensions()[1]

    def get_midpoint(self):
        # returns x-midpoint of the provided image
        return int(math.ceil(self.get_width()/2))

    def get_dimensions(self):
        # returns tuple of (width, height) of the provided image
        image_array_shape = self.image_array.shape
        return image_array_shape[1], image_array_shape[0]

    def get_corners(self):
        # returns tuple of (x1, y1, x2, y2)
        return self.x, self.y, self.x + self.get_width(), self.y + self.get_height()

    def get_pixel(self, x, y):
        return self.pixels[x, y]

    def get_row(self, row_number):
        pixels = []
        for x in range(self.get_width()):
            pixels.append(self.get_pixel(x, row_number))
        return pixels

    def get_column(self, row_number):
        column = []
        image_height = self.get_height(self.image)

        for y in range(image_height):
            column.append(np.asarray(self.image)[y][row_number])

        return self.__numerical_pixels_to_booleans(column)

    def subtract_row(self, y):
        # subtract row as array
        pixels = self.image.load()
        print pixels
        for x in range(self.get_width()):
            pixels[x, y] = 255

        # convert back to image
        self.image = Image.fromarray(self.image_array)

    def erase(self, x, y):
        self.pixels[x, y] = True
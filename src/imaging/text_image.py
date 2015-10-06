from sheet_image_slice import SheetImageSlice


class TextImage(SheetImageSlice):
    def __init__(self, image, x, y):
        # requires head_size as determined by the width of ledger spacing
        super(TextImage, self).__init__(image, x, y)
        self.text = None  # list of y-values for ledger lines
from sheet_image_slice import SheetImageSlice


class NoteImage(SheetImageSlice):
    def __init__(self, image, head_size, x, y):
        # requires head_size as determined by the width of ledger spacing
        super(NoteImage, self).__init__(image, x, y)
        self.head_size = head_size
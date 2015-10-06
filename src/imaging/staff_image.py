from sheet_image_slice import SheetImageSlice


class StaffImage(SheetImageSlice):
    def __init__(self, image, x, y, purpose):
        # requires head_size as determined by the width of ledger spacing
        super(StaffImage, self).__init__(image, x, y)
        self.ledger_line_positions = []  # list of y-values for ledger lines
        self.purpose = purpose # "lyrics", "treble", or "bass"
        self.pitch = None
        self.duration = None

    def __str__(self):
        return "Staff at: " + str((self.x, self.y, self.get_width(), self.get_height())) + " of type: " + self.purpose
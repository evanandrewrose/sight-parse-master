from imaging import sheet_image
import numpy
import unittest

class TestSheetFunctions(unittest.TestCase):
    def setUp(self):
        # prepare numpy
        numpy.set_printoptions(threshold=numpy.nan)
        # create sheet music from mary had a little lamb gif
        self.lamb_sheet = sheet_image.SheetImage('../../bin/mary-had-a-little-lamb.gif')
        # hardcoded test values from marry had a little lamb gif
        self.REAL_WIDTH = 469;
        self.REAL_HEIGHT = 520;
        self.REAL_MIDPOINT = 469/2;

    def test_to_array(self):
        # test that array is not empty or null
        image_array = self.lamb_sheet.get_image_array()
        self.assertTrue(image_array != None)
        self.assertTrue(image_array.size > 0)

    def test_dimensions(self):
        # test that the correct midpoint of width is found
        width = self.lamb_sheet.get_width()
        height = self.lamb_sheet.get_height()
        midpoint = self.lamb_sheet.get_midpoint()

        self.assertTrue((width == self.REAL_WIDTH),
            ("Width Found: " + str(width) + 
            ", expected: " + str(self.REAL_WIDTH)))
        self.assertTrue((height == self.REAL_HEIGHT),
            ("Height Found: " + str(height) + 
            ", expected: " + str(self.REAL_HEIGHT)))
        self.assertTrue((midpoint == self.REAL_MIDPOINT),
            ("Midpoint Found: " + str(midpoint) + 
            ", expected: " + str(self.REAL_MIDPOINT)))

if __name__ == '__main__':
    unittest.main()

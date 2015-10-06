from PIL import Image
import math
import numpy as np
from sheet_image_slice import SheetImageSlice
from note_image import NoteImage
from noterec import whatNoteIsThis
import itertools
import collections
from src.sheet_music.sheet import Sheet
from src.sheet_music.note import Note
from src.sheet_music.exportMidi import Midi

class SheetImageParser:
    def __init__(self, source_image_path):
        # Constants
        self.LEDGER_LINE_MAX_THICKNESS = 2

        self.whole_image = SheetImageSlice(Image.open(source_image_path))
        #self.staffs = self.find_staffs()  # list of StaffImages representing staff positions
        self.notes = []  # list of Notes
        self.header = None  # if non-None, the main header text (usually title)
        self.subheader = None  # if non-None, the sub header text (usually author)
        self.other_texts = []  # list of other texts found
        self.ledger_dict = {} # y-values -> pitch values
        self.ledger_lines = []
        self.build_ledger_dict()
        self.erase_ledger_lines()
        self.get_notes()

    def __ascii_image(self):
        for y in range(self.whole_image.get_height()):
            line = ""
            for x in range(self.whole_image.get_width()):
                line += "_" if self.whole_image.get_pixel(x, y) else "1"

    def get_ledger_lines(self):
        # returns a list of y-positions where there are black, horizontal lines

        # we'll assume a line is anything that is 20% of the width of the image,
        # is located at the center, and has a spacing of at least 3 pixels from
        # the last line examined.
        horizontal_lines = []
        midpoint = self.whole_image.get_midpoint()

        iterator_y = range(self.whole_image.get_height()).__iter__()
        for y in iterator_y:
            # if the center pixel is not black, it's not a line
            if self.whole_image.get_pixel(midpoint, y): # pixel is white
                continue

            current_row = self.whole_image.get_row(y)
            x_begin = int(self.whole_image.get_midpoint() - int(self.whole_image.get_width()*.1))
            x_end = int(self.whole_image.get_midpoint() + int(self.whole_image.get_width()*.1))
            expected_width = int(x_end-x_begin)

            if current_row[x_begin:x_end].count(False) == expected_width:
                horizontal_lines.append(y)

                collections.deque(itertools.islice(iterator_y, self.LEDGER_LINE_MAX_THICKNESS))

        self.ledger_lines = horizontal_lines

        return horizontal_lines

    def build_ledger_dict(self):
        ledger_lines = self.get_ledger_lines()

        # get distance between ledger lines
        ledger_distance = ledger_lines[1] - ledger_lines[0]
        half_distance = int(ledger_distance/2)
        for i, line in enumerate(ledger_lines):
            if (i+1) % 5 == 1:
                self.ledger_dict[line - half_distance] = 'G3'
                self.ledger_dict[line] = 'F3'
                self.ledger_dict[line + half_distance] = 'E3'
            elif (i+1) % 5 == 2:
                self.ledger_dict[line] = 'D3'
                self.ledger_dict[line + half_distance] = 'C3'
            elif (i+1) % 5 == 3:
                self.ledger_dict[line] = 'B3'
                self.ledger_dict[line + half_distance] = 'A4'
            elif (i+1) % 5 == 4:
                self.ledger_dict[line] = 'G4'
                self.ledger_dict[line + half_distance] = 'F4'
            elif (i+1) % 5 == 0:
                self.ledger_dict[line] = 'E4'
                self.ledger_dict[line + half_distance] = 'D4'
                self.ledger_dict[line + half_distance*2] = 'C4'

    def erase_ledger_lines(self):
        # how many are there
        counts = []
        for x in range(self.whole_image.get_width()):
            count = 0
            for y in range(self.whole_image.get_height()):
                if not self.whole_image.get_pixel(x, y):
                    count += 1
            counts.append(count)

        total = collections.Counter(counts).most_common(1)[0][0]

        # where are they
        locations = []

        for x in range(self.whole_image.get_width()):
            count = 0
            blacks_found = []
            for y in range(self.whole_image.get_height()):
                if not self.whole_image.get_pixel(x, y):
                    count += 1
                    blacks_found.append(y)
            if count == total:
                locations = blacks_found
                break

        # erase
        for y in locations:
            for x in range(self.whole_image.get_width()):
                if self.whole_image.get_pixel(x, y-2) or self.whole_image.get_pixel(x, y+2):
                    self.whole_image.erase(x, y)

        # testing
        self.whole_image.image.save("test.gif")

    def get_notes(self):
        # returns list of note images
        checked = [] # list of rectangle tuples of areas we've already examined
        notes = [] # list of NoteImage notes
        ledgers = sorted(self.ledger_lines)
        top_y = ledgers[0]
        bottom_y = ledgers[-1]
        left_x = 3
        right_x = self.whole_image.get_width()-3
        head_size = ledgers[1] - ledgers[0]

        imaginary_borders = []

        begin = None
        end = None

        for i, y in enumerate(ledgers):
            if (i+1) % 5 == 1:
                begin = y
            if (i+1) % 5 == 0:
                end = y
                distance = end - begin
                buffer = distance/2
                imaginary_borders.append((begin-buffer, end+buffer))

        for borders in imaginary_borders:
            for x in range(left_x, right_x):
                for y in range(borders[0], borders[1]):
                    # make sure we didn't check this pixel already
                    already_checked = False
                    for rect in checked:
                        if x >= rect[0] and x <= rect[0]+rect[2]:
                            if y >= rect[1] and y <= rect[1] + rect[3]:
                                already_checked = True
                                break

                    if already_checked:
                        continue

                    if not self.whole_image.get_pixel(x, y):
                        # begin boxing out note
                        top_left = {"x": x, "y": y}
                        bottom_right = {"x": x+1, "y": y+1}
                        search_over = False
                        while not search_over:
                            search_over = True
                            # look up
                            for xi in range(top_left["x"]-1, bottom_right["x"]+1):
                                if not self.whole_image.get_pixel(xi, top_left["y"]-1):
                                    search_over = False
                                    top_left["y"] -= 1
                                    break
                            # look down
                            for xi in range(top_left["x"]-1, bottom_right["x"]+1):
                                if not self.whole_image.get_pixel(xi, bottom_right["y"]+1):
                                    search_over = False
                                    bottom_right["y"] += 1
                                    break
                            # look left
                            for yi in range(top_left["y"]-1, bottom_right["y"]+1):
                                if not self.whole_image.get_pixel(top_left["x"]-1, yi):
                                    search_over = False
                                    top_left["x"] -= 1
                                    break
                            # look right
                            for yi in range(top_left["y"]-1, bottom_right["y"]+1):
                                if not self.whole_image.get_pixel(bottom_right["x"]+1, yi):
                                    search_over = False
                                    bottom_right["x"] += 1
                                    break
                        # search is over
                        note_x_pos = top_left["x"]
                        note_y_pos = top_left["y"]
                        note_width = abs(bottom_right["x"] - top_left["x"])
                        note_height = abs(bottom_right["y"] - top_left["y"])

                        checked.append([note_x_pos, note_y_pos, note_width, note_height])

                        if note_width > 3 and note_height > 3:
                            note = NoteImage(self.whole_image.slice(note_x_pos, note_y_pos, note_width+1, note_height+1),
                                             head_size, note_x_pos + note_width, note_y_pos + note_height - head_size/2)
                            notes.append(note)
        self.notes = notes

    def get_pitch(self, y):
        # get closest line
        lines = self.ledger_dict.keys()
        smallest_difference = None
        note = None

        for line in lines:
            diff = abs(line - y)
            if smallest_difference == None or diff < smallest_difference:
                smallest_difference = diff
                note = self.ledger_dict[line]

        return note

if __name__ == "__main__":
    #sp = SheetImageParser("../../bin/mary-had-a-little-lamb.gif")
    sp = SheetImageParser("../../bin/twinkle-twinkle.gif")

    # write xml
    sheet = Sheet('Twinkle Twinkle Little Star', 'Anon', '2', '4', 'G', '2')

    for i, note_img in enumerate(sp.notes):
        if whatNoteIsThis(note_img.image) == None:
            continue
        else:
            pitch = sp.get_pitch(note_img.y)[0]
            octave = sp.get_pitch(note_img.y)[1]
            duration = {
                'whole' : 1,
                'half' : .5,
                'quarter' : .25,
                'eighth' : .125,
                'sixteenth' : .0625,
                'thirty-second' : .03125,
            }[whatNoteIsThis(note_img.image)]
            note = Note(pitch, octave, duration, False)
            sheet.add_note(note)

    sheet.export_xml()

    # write midi
    m = Midi()

    for i, note_img in enumerate(sp.notes):
        if whatNoteIsThis(note_img.image) == None:
            continue
        else:
            pitch = sp.get_pitch(note_img.y)
            duration = {
                'whole' : 1,
                'half' : .5,
                'quarter' : .25,
                'eighth' : .125,
                'sixteenth' : .0625,
                'thirty-second' : .03125,
            }[whatNoteIsThis(note_img.image)]
            m.add_note(pitch, duration)
    m.write()
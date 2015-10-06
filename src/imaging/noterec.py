from PIL import Image
import numpy as np
from collections import Counter
from os import listdir
from os.path import isfile, join

#image recognition!
def whatNoteIsThis(source_image):
    SIMILARITY_REQUIREMENT = .6
    image_path = "./newimages/"
    # convert source to b/w
    source_image.convert("1")
    source_array = source_image.load()

    image_files = [f for f in listdir(image_path) if isfile(join(image_path,f))]
    similarities = {}

    for image_file in image_files:
        image = Image.open(image_path + image_file)
        # resize
        image = image.resize(source_image.size, Image.ANTIALIAS)
        # change to b/w
        image.convert('1')
        image_array = image.load()
        # compare
        similarity = 0
        for x in range(source_image.size[0]):
            for y in range(source_image.size[1]):
                similarity += 1 if source_array[x, y] == image_array[x, y] else 0
        similarities[image_file] = similarity

    match = max(similarities, key=similarities.get)
    max_similarity = source_image.size[0]*source_image.size[1]
    percent_similarity = max(similarities.values())*1.0/max_similarity

    # if percent_similarity is too small, just return None indicating no match
    if percent_similarity < SIMILARITY_REQUIREMENT:
        return None

    #print "Percent similarity: " + str(percent_similarity) + "%"

    first_character = match[0]

    return {"w":"whole", "h":"half", "q":"quarter"}[first_character]

if __name__=="__main__":
    whatNoteIsThis("test")

# Copyright (C) 2015 kwadrat
# License: http://www.gnu.org/licenses/gpl.html GPL version 2 or higher

#A simple project inspired by Zbigniew Rybczyński's short film Kwadrat (Square).
#Watch the film: http://artmuseum.pl/pl/filmoteka/praca/rybczynski-zbigniew-kwadrat
#Read a description: http://www.zbigvision.com/Kwadrat.html
#ZBIG VISION website: http://www.zbigvision.com/
#kwadrat lets you turn a set of images in a set of frames following the process used by Zbig Rybczyński when making the short film Kwadrat in 1972.
#0) For every picture in the loop
#1) Take a square picture of size l
    #2) Build a grid of size l on top of the image
        #3) For every (square) cell in the grid
            #4) If the cell intersects part of the underlying image, draw a WHITE square
            #5) If the cell does not intersect part of the underlying image, draw a BLACK square
    #) Change l to l/2
    #) Repeat from 2

from PIL import Image
from PIL import ImageFilter
import sys

#kwadrat code
KWADRAT_BLACK = 0
KWADRAT_WHITE = 255
KWADRAT_PROGRAM_NAME = "kwadrat"
KWADRAT_BASE_OUTPUT_FILE_NAME = "kwadrat"

def get_max_value_in_range(range_w, range_h, img):
    max = 0
    for x in xrange(range_w[0], range_w[1]):
        for y in xrange(range_h[0], range_h[1]):
            current = img.getpixel((x, y))
            if current > max:
                max = current
    return max

def set_value_in_range(range_w, range_h, value, img):
    for x in xrange(range_w[0], range_w[1]):
        for y in xrange(range_h[0], range_h[1]):
            img.putpixel((x, y), value);

def save_kwadrat_photograph(sequence, current_length, img):
    filename = "{}_{}_{}-{}.png".format(str(sequence).zfill(4), KWADRAT_BASE_OUTPUT_FILE_NAME, str(current_length), str(current_length))
    img.save(filename)

#assumptions
#1) all square images of same size (power of 2 size)
#2) pixel values are 0 or 255 (e.g.: black or white pixels only)
def make_kwadrat(photographs):
    sequence = 0
    size = photographs[0].size
    length = size[0]
    current_length = length
    while current_length > 0:
        ratio = length/current_length
        for photograph in photographs:
            #for size 1, there's no need to go through the computation, just save the image as is.
            if current_length == 1:
                save_kwadrat_photograph(sequence, current_length, photograph)
                sequence += 1
                continue
            photograph_copy = photograph.copy()
            for x in xrange(0,(ratio)):
                w_left = length/ratio*x
                w_right = length/ratio*(x+1)
                for y in xrange(0,(ratio)):
                    h_left = length/ratio*y
                    h_right = length/ratio*(y+1)
                    max = get_max_value_in_range((w_left, w_right), (h_left, h_right), photograph_copy)
                    if max == 0:
                        set_value_in_range((w_left, w_right), (h_left, h_right), KWADRAT_BLACK, photograph_copy)
                    else:
                        set_value_in_range((w_left, w_right), (h_left, h_right), KWADRAT_WHITE, photograph_copy)
                    print "{} -- iteration: ({}, {}) - ({}, {}) - {}".format(KWADRAT_PROGRAM_NAME, w_left, w_right, h_left, h_right, max)
            save_kwadrat_photograph(sequence, current_length, photograph_copy)
            sequence += 1
        current_length = current_length/2

##BEGIN
photographs = []
for i in range(1, len(sys.argv)):
    photograph_name = sys.argv[i]
    im = Image.open(photograph_name)
    imbwedsm = im.convert("L")
    imbwedsm = imbwedsm.point(lambda x: 255 if x > 255/2 else 0)
    #imbwed = imbw.filter(ImageFilter.FIND_EDGES)
    #imbwedsm = imbwed.filter(ImageFilter.SMOOTH)
    photographs.append(imbwedsm)
if len(photographs) > 0:
    make_kwadrat(photographs)
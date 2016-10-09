from skimage import transform
import numpy as np
import re

PREFIX = 'zoom'
REGEX = re.compile(r"^" + PREFIX + "_(?P<p1x>[-0-9]+)_(?P<p1y>[-0-9]+)_(?P<p2x>[-0-9]+)_(?P<p2y>[-0-9]+)")
PAD_VALUE = 0

class Zoom:
    def __init__(self, p1x, p1y, p2x, p2y):
        self.p1x = p1x
        self.p1y = p1y
        self.p2x = p2x
        self.p2y = p2y
        self.code = PREFIX + str(p1x) + '_' + str(p1y) + '_' + str(p2x) + '_' + str(p2y)

    def process(self, img):
        h = len(img)
        w = len(img[0])

        crop_p1x = max(self.p1x, 0)
        crop_p1y = max(self.p1y, 0)
        crop_p2x = min(self.p2x, w)
        crop_p2y = min(self.p2y, h)

        cropped_img = img[crop_p1y:crop_p2y, crop_p1x:crop_p2x]

        x_pad_before = -min(0, self.p1x)
        x_pad_after  =  max(0, self.p2x-w)
        y_pad_before = -min(0, self.p1y)
        y_pad_after  =  max(0, self.p2y-h)

        padding = [(y_pad_before, y_pad_after), (x_pad_before, x_pad_after)]
        is_colour = len(img.shape) == 3
        if is_colour:
            padding.append((0,0)) # colour images have an extra dimension

        padded_img = np.pad(cropped_img, padding, 'constant')
        return transform.resize(padded_img, (h,w))

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Zoom(int(d['p1x']), int(d['p1y']), int(d['p2x']), int(d['p2y']))
from skimage.filters import gaussian
from skimage.exposure import rescale_intensity
import re

CODE = 'blur'
REGEX = re.compile(r"^" + CODE + "_(?P<sigma>[.0-9]+)")

class Blur:
    def __init__(self, sigma):
        self.code = CODE + str(sigma)
        self.sigma = sigma

    def process(self, img):
        is_colour = len(img.shape)==3
        return rescale_intensity(gaussian(img, sigma=self.sigma, multichannel=is_colour))

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Blur(float(d['sigma']))

from skimage import transform
import re

PREFIX = 'rot'

class Rotate:
    def __init__(self, angle):
        self.angle = angle
        self.code = PREFIX + str(angle)

    def process(self, img):
        return transform.rotate(img, -self.angle)

    @staticmethod
    def match_code(code):
        if code.startswith(PREFIX):
            angle = int(code[len(PREFIX):])
            return Rotate(angle)
import numpy as np

CODE = 'fliph'

class FlipH:
    def __init__(self):
        self.code = CODE

    def process(self, img):
        return np.fliplr(img)

    @staticmethod
    def match_code(code):
        if code == CODE:
            return FlipH()
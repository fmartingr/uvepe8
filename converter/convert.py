import ImageChops
import Image

# Export as animation in keynote. Quicktime Lossless RGBA
# Conversion: ffmpeg -i animation.mov -y -vcodec png -pix_fmt rgba test/test_%d.png

# Javascript set timeout:
# DELAY TIMING
# Put setTimeout before exec any code, so timing will be more accurate

# Globals
# Original video FPS
FPS = 30 # Delay timing = 60*1000/FPS miliseconds

CURRENT_FRAME = 0
FRAMES = []
DIFFS = []

class Diff(object):
    """
    Diff Class
    Save DIFF image and MD5 hash of the image to avoid redundancy
    """
    # Variables
    md5 = None
    image = None
    position = ()

    def __init__(self, image, x, y):
        self.image = image

    def set_position(self, x, y):
        self.position = (x, y)

class Frame(object):
    # Variables
    path = None
    image = None
    diff = []
    jump = 0

    # Internal
    difference = None # Difference between this and the previous frame

    def __init__(self, path):
        if not self.opened():
            self.image = Image.open(path)
            self.path = path

    def opened(self):
        return self.image is None

    def get_difference(self):
        if self.difference is None:
            self.difference = ImageChops.difference(self.image, FRAMES[CURRENT_FRAME-1])
        return self.difference



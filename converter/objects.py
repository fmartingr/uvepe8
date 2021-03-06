import Image

class Diff(object):
    """
    Diff Class
    Save DIFF image and MD5 hash of the image to avoid redundancy
    """
    hash = None
    image = None
    position = () # Diff position in the complete image (final png)
    size = () # Size of the image (diff)
    #image_position = () # Position on the original image (where the diff goes)

    # Internals
    controller = None

    def __init__(self, parent_object, image, width, height):
        self.controller = parent_object
        self.image = image
        self.hash = hash
        self.size = (width, height)
        #self.set_original_position(x, y, width, height)

    def set_position(self, x, y):
        self.position = (x, y)

#    def set_original_position(self, x, y, width, height):
#        self.image_position = (x, y)

    def have_image(self):
        return self.image is not None

    def calculate_hash(self):
        if self.have_image():
            self.hash = None

    def width(self):
        return self.size[0]

    def height(self):
        return self.size[1]


class Frame(object):
    """
    Frame Class
    Stores data for each frame that contains changes
    """
    path = None
    image = None
    diff = [] # (diff hash, position x, position y, size x, size y)
    jump = 0

    # Internal
    controller = None
    difference = None

    def __init__(self, parent_object, path):
        self.controller = parent_object
        if not self.opened():
            self.image = Image.open(path)
            self.path = path
        self.diff = []

    def opened(self):
        return self.image is not None

    def add_diff(self, diff):
        self.diff.append(diff)

    def get_difference(self):
        if self.difference is None:
            return self.controller.get_difference(self.image, self.controller.get_previous().image)

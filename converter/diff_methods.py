#from objects import Diff


class DiffMethod(object):
    pass


class SimpleMethod(DiffMethod):
    """
    Simple PIL getbbox() difference between frames
    """
    def difference(self, first, second):
        import ImageChops
        from hashlib import md5
        difference = ImageChops.difference(first, second)
        diff_box = difference.getbbox()
        diffs = []
        if diff_box is not None:
            # If there is any difference, just retrieve the box
            # that has changed in the new frame
            image = first.crop((diff_box[0],
                                     diff_box[1],
                                     diff_box[2],
                                     diff_box[3]))
            size = (diff_box[2] - diff_box[0], diff_box[3] - diff_box[1])
            position = (diff_box[0], diff_box[1])
            hash = str(md5(image.tostring()).hexdigest())
            diff = {
                "hash": hash,  # Hash of the diff for checking if portion is repeated (md5 string)
                "image": image,  # Portion of the image <Image>
                "position": position,  # Position of the portion in the frame (x, y)
                "size": size  # Size of the portion (x, y)
            }
            diffs.append(diff)

        return diffs


class GridMethod(DiffMethod):
    """
    TODO
    Converts frame to grid and compare each grid square with the previous frame square grid
    --
    1) Calc dividers from the frame resolution
    2) Select the bigger one (max: 16?)
    -- or --
    1) Get the square size from parameter (override)
    --
    """
    def __init__(self):
        self.grid_size = (0, 0)
        self.image_size = (0, 0)
        self.grid_size_calculated = False

    def get_divisors(self, number):
        i = 1
        divisors = []
        while i <= number:
            if number % i == 0:
                divisors.append(i)
            i = i + 1
        return divisors

    def get_common_divisors(self, width, height, max_divisor=50):
        width_divisors = [x for x in self.get_divisors(width) if x <= max_divisor]
        height_divisors = [x for x in self.get_divisors(height) if x <= max_divisor]

        # Get common divisor to get grid square size
        common = 1
        for x in width_divisors:
            for y in height_divisors:
                if x == y:
                    common = x
        return (width / common, height / common)

    def calc_grid_size(self, width, height):
        """
        We need to calculate the size of the square tiles
        """
        self.grid_size = self.get_common_divisors(width, height)
        print "Got grid size: %dx%d" % (self.grid_size[0], self.grid_size[1])
        self.image_size = (width, height)
        self.grid_size_calculated = True

    def difference(self, first, second):
        import ImageChops
        from hashlib import md5
        # First frame, calculate grid size
        if self.grid_size_calculated is False:
            self.calc_grid_size(first.size[0], first.size[1])

        diffs = []

        # Current frame position
        current_position = (0, 0)
        while current_position[0] < self.image_size[0]:
            while current_position[1] < self.image_size[1]:
                # Chop, chop...
                chop_parameters = (current_position[0],          # X
                    current_position[1],                         # Y
                    current_position[0] + self.grid_size[0],     # Size X
                    current_position[1] + self.grid_size[1])     # Size Y
                #print chop_parameters
                last = first.crop(chop_parameters)
                current = second.crop(chop_parameters)

                difference = ImageChops.difference(last, current)
                diff_box = difference.getbbox()

                if diff_box is not None:
                    # This portion has changed :D
                    image = current
                    size = self.grid_size
                    position = current_position
                    hash = str(md5(image.tostring()).hexdigest())
                    diff = {
                        "hash": hash,  # Hash of the diff for checking if portion is repeated (md5 string)
                        "image": image,  # Portion of the image <Image>
                        "position": position,  # Position of the portion in the frame (x, y)
                        "size": size  # Size of the portion (x, y)
                    }
                    diffs.append(diff)
                current_position = (current_position[0], current_position[1] + self.grid_size[1])
            current_position = (current_position[0] + self.grid_size[0], 0)
            # TODO find a better way to add to tuples.
        return diffs


class SquaresMethod(DiffMethod):
    """
    TODO
    """
    pass

























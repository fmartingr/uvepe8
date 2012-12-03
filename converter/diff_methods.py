from objects import Diff


class DiffMethod(object):
    def __init__(self):
        self.min_diffrence = 60

class SimpleMethod(DiffMethod):
    """
    Simple PIL getbbox() difference between frames
    """
    def difference(self, actual, previous):
        import ImageChops
        from hashlib import md5
        difference = ImageChops.difference(actual, previous)
        diff_box = difference.getbbox()
        diffs = []
        if diff_box is not None:
            # If there is any difference, just retrieve the box
            # that has changed in the new frame
            image = actual.crop((diff_box[0],
                                     diff_box[1],
                                     diff_box[2],
                                     diff_box[3]))
            size = (diff_box[2] - diff_box[0], diff_box[3] - diff_box[1])
            position = (diff_box[0], diff_box[1])
            hash = str(md5(image.tostring()).hexdigest())
            diff = {
                "hash": hash, # Hash of the diff for checking if portion is repeated (md5 string)
                "image": image, # Portion of the image <Image>
                "position": position, # Position of the portion in the frame (x, y)
                "size": size # Size of the portion (x, y)
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

class SquaresMethod(DiffMethod):
    """
    TODO
    """
    pass
